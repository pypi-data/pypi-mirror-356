#!/usr/bin/env python3
"""
MCP Server for Cloudeka CLI (cldkctl) functionality.
"""

import asyncio
import json
import os
import sys
from typing import Any, Dict, List, Optional, Sequence
import requests
import base64
from datetime import datetime, timedelta

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel,
    Text,
    Image,
    Resource,
    ToolResult,
    Error,
    NotifyErrorRequest,
    ShowMessageRequest,
    MessageType,
    ShowProgressRequest,
    ProgressNotification,
    ProgressNotificationKind,
    TextDocument,
    Position,
    Range,
    Location,
    Diagnostic,
    DiagnosticSeverity,
    PublishDiagnosticsRequest,
    LogMessageRequest,
)

# Initialize the server
server = Server("cldkctl")

# Configuration
PRODUCTION_URL = "https://ai.cloudeka.id"
STAGING_URL = "https://staging.ai.cloudeka.id"
CACHE_FILE = os.path.expanduser("~/.cldkctl/mcp_cache.json")
CACHE_DIR = os.path.expanduser("~/.cldkctl")

# Ensure cache directory exists
os.makedirs(CACHE_DIR, exist_ok=True)

# Global state for authentication and environment
auth_cache = {
    "jwt_token": None,
    "login_payload": None,
    "expires_at": None,
    "user_info": None
}

# Environment configuration
current_base_url = PRODUCTION_URL  # Default to production
environment_name = "production"

def load_cache():
    """Load cached authentication data."""
    global auth_cache
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as f:
                cached_data = json.load(f)
                # Check if token is still valid
                if cached_data.get("expires_at"):
                    expires_at = datetime.fromisoformat(cached_data["expires_at"])
                    if datetime.now() < expires_at:
                        auth_cache.update(cached_data)
                        print(f"Loaded cached auth data, expires at {expires_at}", file=sys.stderr)
                        return True
                    else:
                        print("Cached token expired", file=sys.stderr)
                return False
    except Exception as e:
        print(f"Error loading cache: {e}", file=sys.stderr)
    return False

def save_cache():
    """Save authentication data to cache."""
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(auth_cache, f, default=str)
    except Exception as e:
        print(f"Error saving cache: {e}", file=sys.stderr)

def authenticate_with_token(token: str, force_staging: bool = False) -> bool:
    """Authenticate using a cldkctl token and get JWT."""
    global auth_cache, current_base_url, environment_name
    
    # Use staging if forced or if production failed before
    if force_staging:
        current_base_url = STAGING_URL
        environment_name = "staging"
    else:
        current_base_url = PRODUCTION_URL
        environment_name = "production"
    
    print(f"Authenticating with {environment_name} environment: {current_base_url}", file=sys.stderr)
    print(f"Token: {token[:20]}...", file=sys.stderr)
    
    url = f"{current_base_url}/core/cldkctl/auth"
    payload = {"token": token}
    
    try:
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        print(f"Auth response status: {response.status_code}", file=sys.stderr)
        
        if response.status_code == 200:
            data = response.json()
            jwt_token = data.get("data", {}).get("token")
            if jwt_token:
                # Cache the authentication data
                auth_cache["jwt_token"] = jwt_token
                auth_cache["login_payload"] = base64.b64encode(json.dumps(payload).encode()).decode()
                auth_cache["expires_at"] = (datetime.now() + timedelta(hours=24)).isoformat()
                auth_cache["user_info"] = data.get("data", {})
                auth_cache["environment"] = environment_name
                auth_cache["base_url"] = current_base_url
                save_cache()
                print(f"Authentication successful with {environment_name}", file=sys.stderr)
                return True
            else:
                print("No JWT token in response", file=sys.stderr)
                return False
        elif response.status_code == 400 and "pq: relation \"cldkctl_tokens\" does not exist" in response.text:
            print("Production backend has database issue, trying staging...", file=sys.stderr)
            if not force_staging:
                return authenticate_with_token(token, force_staging=True)
            else:
                print("Both production and staging failed", file=sys.stderr)
                return False
        else:
            print(f"Authentication failed: {response.status_code} - {response.text}", file=sys.stderr)
            return False
    except Exception as e:
        print(f"Authentication error: {e}", file=sys.stderr)
        if not force_staging:
            print("Trying staging as fallback...", file=sys.stderr)
            return authenticate_with_token(token, force_staging=True)
        return False

def get_auth_headers() -> Dict[str, str]:
    """Get headers with authentication token."""
    if not auth_cache["jwt_token"]:
        raise Exception("Not authenticated. Please authenticate first.")
    
    return {
        "Authorization": f"Bearer {auth_cache['jwt_token']}",
        "Content-Type": "application/json"
    }

def make_authenticated_request(method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
    """Make an authenticated request to the API."""
    url = f"{current_base_url}{endpoint}"
    headers = get_auth_headers()
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            raise Exception(f"Unsupported HTTP method: {method}")
        
        if response.status_code == 401:
            # Token expired, try to re-authenticate
            print("Token expired, attempting re-authentication", file=sys.stderr)
            if auth_cache["login_payload"]:
                login_data = json.loads(base64.b64decode(auth_cache["login_payload"]).decode())
                if authenticate_with_token(login_data["token"]):
                    # Retry the request
                    headers = get_auth_headers()
                    if method.upper() == "GET":
                        response = requests.get(url, headers=headers)
                    elif method.upper() == "POST":
                        response = requests.post(url, json=data, headers=headers)
                    elif method.upper() == "PUT":
                        response = requests.put(url, json=data, headers=headers)
                    elif method.upper() == "DELETE":
                        response = requests.delete(url, headers=headers)
                else:
                    raise Exception("Re-authentication failed")
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")

# Load cached auth on startup
load_cache()

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """List all available tools."""
    tools = [
        # Authentication
        Tool(
            name="auth",
            description="Authenticate with a cldkctl token to get JWT access",
            inputSchema={
                "type": "object",
                "properties": {
                    "token": {
                        "type": "string",
                        "description": "Your cldkctl token (starts with 'cldkctl_')"
                    },
                    "force_staging": {
                        "type": "boolean",
                        "description": "Force using staging environment (default: false, will auto-fallback if production fails)"
                    }
                },
                "required": ["token"]
            }
        ),
        
        Tool(
            name="switch_environment",
            description="Switch between production and staging environments",
            inputSchema={
                "type": "object",
                "properties": {
                    "environment": {
                        "type": "string",
                        "description": "Environment to use: 'production' or 'staging'",
                        "enum": ["production", "staging"]
                    }
                },
                "required": ["environment"]
            }
        ),
        
        Tool(
            name="status",
            description="Show current authentication and environment status",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        
        # Balance
        Tool(
            name="balance_detail",
            description="Get balance details for a project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "string",
                        "description": "Project ID"
                    }
                },
                "required": ["project_id"]
            }
        ),
        
        # Billing
        Tool(
            name="billing_daily_cost",
            description="Get daily billing costs for a project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "string",
                        "description": "Project ID"
                    }
                },
                "required": ["project_id"]
            }
        ),
        
        Tool(
            name="billing_monthly_cost",
            description="Get monthly billing costs for a project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "string",
                        "description": "Project ID"
                    }
                },
                "required": ["project_id"]
            }
        ),
        
        Tool(
            name="billing_history",
            description="Get billing history",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "string",
                        "description": "Project ID (optional)"
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Start date (YYYY-MM-DD)"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date (YYYY-MM-DD)"
                    }
                }
            }
        ),
        
        # Kubernetes
        Tool(
            name="k8s_pods",
            description="List Kubernetes pods in a namespace",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "string",
                        "description": "Project ID"
                    },
                    "namespace": {
                        "type": "string",
                        "description": "Namespace (default: 'default')"
                    }
                },
                "required": ["project_id"]
            }
        ),
        
        Tool(
            name="k8s_deployments",
            description="List Kubernetes deployments in a namespace",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "string",
                        "description": "Project ID"
                    },
                    "namespace": {
                        "type": "string",
                        "description": "Namespace (default: 'default')"
                    }
                },
                "required": ["project_id"]
            }
        ),
        
        Tool(
            name="k8s_services",
            description="List Kubernetes services in a namespace",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "string",
                        "description": "Project ID"
                    },
                    "namespace": {
                        "type": "string",
                        "description": "Namespace (default: 'default')"
                    }
                },
                "required": ["project_id"]
            }
        ),
        
        Tool(
            name="k8s_configmaps",
            description="List Kubernetes configmaps in a namespace",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "string",
                        "description": "Project ID"
                    },
                    "namespace": {
                        "type": "string",
                        "description": "Namespace (default: 'default')"
                    }
                },
                "required": ["project_id"]
            }
        ),
        
        Tool(
            name="k8s_secrets",
            description="List Kubernetes secrets in a namespace",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "string",
                        "description": "Project ID"
                    },
                    "namespace": {
                        "type": "string",
                        "description": "Namespace (default: 'default')"
                    }
                },
                "required": ["project_id"]
            }
        ),
        
        # Projects
        Tool(
            name="project_list",
            description="List all projects in the organization",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        
        Tool(
            name="project_detail",
            description="Get details of a specific project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "string",
                        "description": "Project ID"
                    }
                },
                "required": ["project_id"]
            }
        ),
        
        # Organization
        Tool(
            name="org_detail",
            description="Get organization details",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        
        Tool(
            name="org_members",
            description="List organization members",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        
        # User Profile
        Tool(
            name="profile_detail",
            description="Get user profile details",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        
        # Virtual Machines
        Tool(
            name="vm_list",
            description="List virtual machines",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "string",
                        "description": "Project ID"
                    }
                },
                "required": ["project_id"]
            }
        ),
        
        Tool(
            name="vm_detail",
            description="Get virtual machine details",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "string",
                        "description": "Project ID"
                    },
                    "vm_id": {
                        "type": "string",
                        "description": "Virtual Machine ID"
                    }
                },
                "required": ["project_id", "vm_id"]
            }
        ),
        
        # Registry
        Tool(
            name="registry_list",
            description="List container registries",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "string",
                        "description": "Project ID"
                    }
                },
                "required": ["project_id"]
            }
        ),
        
        Tool(
            name="registry_repositories",
            description="List repositories in a registry",
            inputSchema={
                "type": "object",
                "properties": {
                    "registry_id": {
                        "type": "string",
                        "description": "Registry ID"
                    }
                },
                "required": ["registry_id"]
            }
        ),
        
        # Notebooks
        Tool(
            name="notebook_list",
            description="List Deka notebooks",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        
        Tool(
            name="notebook_create",
            description="Create a new Deka notebook",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Notebook name"
                    },
                    "image": {
                        "type": "string",
                        "description": "Docker image to use"
                    },
                    "cpu": {
                        "type": "string",
                        "description": "CPU specification (e.g., '1')"
                    },
                    "memory": {
                        "type": "string",
                        "description": "Memory specification (e.g., '2Gi')"
                    },
                    "gpu": {
                        "type": "string",
                        "description": "GPU specification (optional)"
                    }
                },
                "required": ["name", "image", "cpu", "memory"]
            }
        ),
        
        # Vouchers
        Tool(
            name="voucher_list",
            description="List available vouchers",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        
        Tool(
            name="voucher_apply",
            description="Apply a voucher code",
            inputSchema={
                "type": "object",
                "properties": {
                    "voucher_code": {
                        "type": "string",
                        "description": "Voucher code to apply"
                    }
                },
                "required": ["voucher_code"]
            }
        ),
        
        # Logs
        Tool(
            name="audit_logs",
            description="Get audit logs",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string",
                        "description": "Start date (YYYY-MM-DD)"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date (YYYY-MM-DD)"
                    },
                    "action": {
                        "type": "string",
                        "description": "Filter by action type"
                    }
                }
            }
        ),
        
        # Token Management
        Tool(
            name="token_list",
            description="List cldkctl tokens",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        
        Tool(
            name="token_create",
            description="Create a new cldkctl token",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Token name"
                    },
                    "expired": {
                        "type": "string",
                        "description": "Expiration (days or DD/MM/YYYY format)"
                    }
                },
                "required": ["name", "expired"]
            }
        ),
        
        Tool(
            name="token_delete",
            description="Delete a cldkctl token",
            inputSchema={
                "type": "object",
                "properties": {
                    "token_id": {
                        "type": "string",
                        "description": "Token ID to delete"
                    }
                },
                "required": ["token_id"]
            }
        ),
    ]
    
    return ListToolsResult(tools=tools)

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls."""
    global current_base_url, environment_name
    
    try:
        if name == "auth":
            token = arguments["token"]
            force_staging = arguments.get("force_staging", False)
            
            if authenticate_with_token(token, force_staging):
                env_info = f" ({environment_name})" if environment_name != "production" else ""
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text=f"✅ Authentication successful{env_info}!\n\nUser: {auth_cache['user_info'].get('name', 'Unknown')}\nRole: {auth_cache['user_info'].get('role', 'Unknown')}\nOrganization: {auth_cache['user_info'].get('organization_id', 'None')}\nEnvironment: {environment_name}\nBase URL: {current_base_url}"
                        )
                    ]
                )
            else:
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text="❌ Authentication failed. Please check your token or try using staging environment."
                        )
                    ]
                )
        
        elif name == "switch_environment":
            env = arguments["environment"]
            
            if env == "production":
                current_base_url = PRODUCTION_URL
                environment_name = "production"
            elif env == "staging":
                current_base_url = STAGING_URL
                environment_name = "staging"
            else:
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text="❌ Invalid environment. Use 'production' or 'staging'."
                        )
                    ]
                )
            
            # Clear cached auth when switching environments
            auth_cache["jwt_token"] = None
            auth_cache["expires_at"] = None
            save_cache()
            
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"✅ Switched to {environment_name} environment: {current_base_url}\n\nNote: You'll need to re-authenticate."
                    )
                ]
            )
        
        elif name == "status":
            status_text = f"**Environment Status**\n"
            status_text += f"Current Environment: {environment_name}\n"
            status_text += f"Base URL: {current_base_url}\n\n"
            
            if auth_cache["jwt_token"]:
                expires_at = datetime.fromisoformat(auth_cache["expires_at"]) if auth_cache["expires_at"] else None
                status_text += f"**Authentication Status**\n"
                status_text += f"✅ Authenticated\n"
                status_text += f"User: {auth_cache['user_info'].get('name', 'Unknown')}\n"
                status_text += f"Role: {auth_cache['user_info'].get('role', 'Unknown')}\n"
                if expires_at:
                    status_text += f"Token Expires: {expires_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
                    if datetime.now() < expires_at:
                        status_text += f"Status: ✅ Valid\n"
                    else:
                        status_text += f"Status: ❌ Expired\n"
            else:
                status_text += f"**Authentication Status**\n"
                status_text += f"❌ Not authenticated\n"
            
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=status_text
                    )
                ]
            )
        
        elif name == "balance_detail":
            project_id = arguments["project_id"]
            data = make_authenticated_request("GET", f"/core/balance/accumulated/{project_id}")
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Balance Details for Project {project_id}:\n{json.dumps(data, indent=2)}"
                    )
                ]
            )
        
        elif name == "billing_daily_cost":
            project_id = arguments["project_id"]
            data = make_authenticated_request("GET", f"/core/billing/v2/daily-cost/{project_id}")
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Daily Billing Costs for Project {project_id}:\n{json.dumps(data, indent=2)}"
                    )
                ]
            )
        
        elif name == "billing_monthly_cost":
            project_id = arguments["project_id"]
            data = make_authenticated_request("GET", f"/core/billing/monthly-cost/total-billed/{project_id}")
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Monthly Billing Costs for Project {project_id}:\n{json.dumps(data, indent=2)}"
                    )
                ]
            )
        
        elif name == "billing_history":
            payload = {}
            if "project_id" in arguments:
                payload["project_id"] = arguments["project_id"]
            if "start_date" in arguments:
                payload["start_date"] = arguments["start_date"]
            if "end_date" in arguments:
                payload["end_date"] = arguments["end_date"]
            
            data = make_authenticated_request("POST", "/core/billing/v2/history", payload)
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Billing History:\n{json.dumps(data, indent=2)}"
                    )
                ]
            )
        
        elif name == "k8s_pods":
            project_id = arguments["project_id"]
            namespace = arguments.get("namespace", "default")
            data = make_authenticated_request("GET", f"/core/kubernetes/{project_id}/{namespace}/pods")
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Kubernetes Pods in {namespace}:\n{json.dumps(data, indent=2)}"
                    )
                ]
            )
        
        elif name == "k8s_deployments":
            project_id = arguments["project_id"]
            namespace = arguments.get("namespace", "default")
            data = make_authenticated_request("GET", f"/core/kubernetes/{project_id}/{namespace}/deployments")
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Kubernetes Deployments in {namespace}:\n{json.dumps(data, indent=2)}"
                    )
                ]
            )
        
        elif name == "k8s_services":
            project_id = arguments["project_id"]
            namespace = arguments.get("namespace", "default")
            data = make_authenticated_request("GET", f"/core/kubernetes/{project_id}/{namespace}/services")
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Kubernetes Services in {namespace}:\n{json.dumps(data, indent=2)}"
                    )
                ]
            )
        
        elif name == "k8s_configmaps":
            project_id = arguments["project_id"]
            namespace = arguments.get("namespace", "default")
            data = make_authenticated_request("GET", f"/core/kubernetes/{project_id}/{namespace}/configmaps")
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Kubernetes ConfigMaps in {namespace}:\n{json.dumps(data, indent=2)}"
                    )
                ]
            )
        
        elif name == "k8s_secrets":
            project_id = arguments["project_id"]
            namespace = arguments.get("namespace", "default")
            data = make_authenticated_request("GET", f"/core/kubernetes/{project_id}/{namespace}/secrets")
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Kubernetes Secrets in {namespace}:\n{json.dumps(data, indent=2)}"
                    )
                ]
            )
        
        elif name == "project_list":
            data = make_authenticated_request("GET", "/core/user/organization/projects/byOrg")
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Projects:\n{json.dumps(data, indent=2)}"
                    )
                ]
            )
        
        elif name == "project_detail":
            project_id = arguments["project_id"]
            data = make_authenticated_request("GET", f"/core/user/project/detail/{project_id}")
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Project Details:\n{json.dumps(data, indent=2)}"
                    )
                ]
            )
        
        elif name == "org_detail":
            data = make_authenticated_request("GET", "/core/user/organization")
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Organization Details:\n{json.dumps(data, indent=2)}"
                    )
                ]
            )
        
        elif name == "org_members":
            data = make_authenticated_request("GET", "/core/user/organization/member")
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Organization Members:\n{json.dumps(data, indent=2)}"
                    )
                ]
            )
        
        elif name == "profile_detail":
            data = make_authenticated_request("GET", "/core/user/profile")
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Profile Details:\n{json.dumps(data, indent=2)}"
                    )
                ]
            )
        
        elif name == "vm_list":
            project_id = arguments["project_id"]
            data = make_authenticated_request("GET", f"/core/virtual-machine/{project_id}")
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Virtual Machines:\n{json.dumps(data, indent=2)}"
                    )
                ]
            )
        
        elif name == "vm_detail":
            project_id = arguments["project_id"]
            vm_id = arguments["vm_id"]
            data = make_authenticated_request("GET", f"/core/virtual-machine/{project_id}/{vm_id}")
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Virtual Machine Details:\n{json.dumps(data, indent=2)}"
                    )
                ]
            )
        
        elif name == "registry_list":
            project_id = arguments["project_id"]
            data = make_authenticated_request("GET", f"/core/dekaregistry/v2/{project_id}")
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Container Registries:\n{json.dumps(data, indent=2)}"
                    )
                ]
            )
        
        elif name == "registry_repositories":
            registry_id = arguments["registry_id"]
            data = make_authenticated_request("GET", f"/core/dekaregistry/v2/repository/{registry_id}")
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Registry Repositories:\n{json.dumps(data, indent=2)}"
                    )
                ]
            )
        
        elif name == "notebook_list":
            data = make_authenticated_request("GET", "/core/deka-notebook")
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Deka Notebooks:\n{json.dumps(data, indent=2)}"
                    )
                ]
            )
        
        elif name == "notebook_create":
            payload = {
                "name": arguments["name"],
                "image": arguments["image"],
                "cpu": arguments["cpu"],
                "memory": arguments["memory"]
            }
            if "gpu" in arguments:
                payload["gpu"] = arguments["gpu"]
            
            data = make_authenticated_request("POST", "/core/deka-notebook", payload)
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Notebook Created:\n{json.dumps(data, indent=2)}"
                    )
                ]
            )
        
        elif name == "voucher_list":
            data = make_authenticated_request("GET", "/core/voucher")
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Available Vouchers:\n{json.dumps(data, indent=2)}"
                    )
                ]
            )
        
        elif name == "voucher_apply":
            voucher_code = arguments["voucher_code"]
            data = make_authenticated_request("POST", "/core/voucher/apply", {"voucher_code": voucher_code})
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Voucher Applied:\n{json.dumps(data, indent=2)}"
                    )
                ]
            )
        
        elif name == "audit_logs":
            payload = {}
            if "start_date" in arguments:
                payload["start_date"] = arguments["start_date"]
            if "end_date" in arguments:
                payload["end_date"] = arguments["end_date"]
            if "action" in arguments:
                payload["action"] = arguments["action"]
            
            data = make_authenticated_request("POST", "/core/auditlog", payload)
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Audit Logs:\n{json.dumps(data, indent=2)}"
                    )
                ]
            )
        
        elif name == "token_list":
            data = make_authenticated_request("GET", "/core/cldkctl/token")
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Cldkctl Tokens:\n{json.dumps(data, indent=2)}"
                    )
                ]
            )
        
        elif name == "token_create":
            payload = {
                "name": arguments["name"],
                "expired": arguments["expired"]
            }
            data = make_authenticated_request("POST", "/core/cldkctl/token", payload)
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Token Created:\n{json.dumps(data, indent=2)}"
                    )
                ]
            )
        
        elif name == "token_delete":
            token_id = arguments["token_id"]
            data = make_authenticated_request("DELETE", f"/core/cldkctl/token/{token_id}")
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Token Deleted:\n{json.dumps(data, indent=2)}"
                    )
                ]
            )
        
        else:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Unknown tool: {name}"
                    )
                ]
            )
    
    except Exception as e:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )
            ]
        )

async def main():
    """Main function."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="cldkctl",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())