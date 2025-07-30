#!/usr/bin/env python3
"""
MCP Server for Cloudeka CLI (cldkctl) functionality.
"""

import asyncio
import base64
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import requests
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import CallToolResult, ListToolsResult, TextContent, Tool

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
    "user_info": None,
    "environment": "production",
    "base_url": PRODUCTION_URL,
}

# Environment configuration
current_base_url = PRODUCTION_URL  # Default to production
environment_name = "production"


def load_cache():
    """Load cached authentication data."""
    global auth_cache, current_base_url, environment_name
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                cached_data = json.load(f)
                # Check if token is still valid
                if cached_data.get("expires_at"):
                    expires_at = datetime.fromisoformat(cached_data["expires_at"])
                    if datetime.now() < expires_at:
                        auth_cache.update(cached_data)
                        current_base_url = auth_cache["base_url"]
                        environment_name = auth_cache["environment"]
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
        with open(CACHE_FILE, "w") as f:
            json.dump(auth_cache, f, default=str)
    except Exception as e:
        print(f"Error saving cache: {e}", file=sys.stderr)


def authenticate_with_token(token: str, force_staging: bool = False) -> bool:
    """Authenticate using a cldkctl token and get JWT."""
    global auth_cache, current_base_url, environment_name

    # Determine which URL to use
    if force_staging:
        base_url = STAGING_URL
        env_name = "staging"
    else:
        base_url = PRODUCTION_URL
        env_name = "production"

    print(f"Authenticating with {env_name} environment: {base_url}", file=sys.stderr)
    url = f"{base_url}/core/cldkctl/auth"
    payload = {"token": token}

    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        print(f"Auth response status: {response.status_code}", file=sys.stderr)

        if response.status_code == 200:
            data = response.json()
            jwt_token = data.get("data", {}).get("token")
            if jwt_token:
                # Update global state
                current_base_url = base_url
                environment_name = env_name
                # Cache the authentication data
                auth_cache["jwt_token"] = jwt_token
                auth_cache["login_payload"] = base64.b64encode(json.dumps(payload).encode()).decode()
                auth_cache["expires_at"] = (datetime.now() + timedelta(hours=24)).isoformat()
                auth_cache["user_info"] = data.get("data", {})
                auth_cache["environment"] = env_name
                auth_cache["base_url"] = base_url
                save_cache()
                print(f"Authentication successful with {env_name}", file=sys.stderr)
                return True
            else:
                print("No JWT token in response", file=sys.stderr)
                return False
        elif response.status_code == 400 and "pq: relation \"cldkctl_tokens\" does not exist" in response.text:
            print("Production backend has database issue, trying staging...", file=sys.stderr)
            if not force_staging:
                return authenticate_with_token(token, force_staging=True)
            else:
                print("Staging also failed with the same issue.", file=sys.stderr)
                return False
        else:
            print(f"Authentication failed: {response.status_code} - {response.text}", file=sys.stderr)
            return False
    except requests.RequestException as e:
        print(f"Authentication request error: {e}", file=sys.stderr)
        if not force_staging:
            print("Trying staging as fallback...", file=sys.stderr)
            return authenticate_with_token(token, force_staging=True)
        return False


def get_auth_headers() -> Dict[str, str]:
    """Get headers with authentication token."""
    if not auth_cache.get("jwt_token"):
        raise Exception("Not authenticated. Please authenticate first.")

    # Check for token expiration
    expires_at_str = auth_cache.get("expires_at")
    if expires_at_str:
        if datetime.now() >= datetime.fromisoformat(expires_at_str):
            print("Token expired, attempting re-authentication", file=sys.stderr)
            if auth_cache.get("login_payload"):
                login_data = json.loads(base64.b64decode(auth_cache["login_payload"]).decode())
                if not authenticate_with_token(login_data["token"], force_staging=(environment_name == "staging")):
                    raise Exception("Re-authentication failed")
            else:
                raise Exception("Token expired and no login payload to re-authenticate.")

    return {
        "Authorization": f"Bearer {auth_cache['jwt_token']}",
        "Content-Type": "application/json",
    }


def make_authenticated_request(method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
    """Make an authenticated request to the API."""
    url = f"{current_base_url}{endpoint}"
    try:
        headers = get_auth_headers()
        response = requests.request(method, url, headers=headers, json=data, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Authenticated request failed: {e}", file=sys.stderr)
        # In case of an error, return a structured error message
        return {"error": True, "message": str(e), "status_code": getattr(e.response, "status_code", None)}


# Load cached auth on startup
load_cache()


def get_tool_definitions() -> list[Tool]:
    # ... (Keep all tool definitions as they were, just return them from this function)
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
    return tools


@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """List all available tools."""
    return ListToolsResult(tools=get_tool_definitions())


def format_response(data: Any) -> str:
    """Formats API response data for display."""
    if isinstance(data, dict) and data.get("error"):
        return f"❌ API Error: {data.get('message', 'Unknown error')}"
    return f"```json\n{json.dumps(data, indent=2)}\n```"


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
                user_info = auth_cache.get('user_info', {})
                text = (
                    f"✅ Authentication successful{env_info}!\n\n"
                    f"User: {user_info.get('name', 'Unknown')}\n"
                    f"Role: {user_info.get('role', 'Unknown')}\n"
                    f"Organization: {user_info.get('organization_id', 'None')}\n"
                    f"Environment: {environment_name}\n"
                    f"Base URL: {current_base_url}"
                )
                return CallToolResult(content=[TextContent(type="text", text=text)])
            else:
                return CallToolResult(content=[TextContent(type="text", text="❌ Authentication failed.")])

        elif name == "switch_environment":
            env = arguments["environment"]
            if env in ["production", "staging"]:
                current_base_url = PRODUCTION_URL if env == "production" else STAGING_URL
                environment_name = env
                auth_cache.update({"jwt_token": None, "expires_at": None, "environment": env, "base_url": current_base_url})
                save_cache()
                text = f"✅ Switched to {environment_name} environment. You may need to re-authenticate."
            else:
                text = "❌ Invalid environment. Use 'production' or 'staging'."
            return CallToolResult(content=[TextContent(type="text", text=text)])

        elif name == "status":
            status_text = f"**Environment Status**\n- **Environment:** {environment_name}\n- **Base URL:** {current_base_url}\n\n"
            if auth_cache.get("jwt_token"):
                expires_at = datetime.fromisoformat(auth_cache["expires_at"]) if auth_cache["expires_at"] else None
                status_text += f"**Authentication Status**\n- **Status:** ✅ Authenticated\n"
                status_text += f"- **User:** {auth_cache.get('user_info', {}).get('name', 'Unknown')}\n"
                if expires_at:
                    status_text += f"- **Token Expires:** {expires_at.strftime('%Y-%m-%d %H:%M:%S')}"
            else:
                status_text += f"**Authentication Status**\n- **Status:** ❌ Not authenticated"
            return CallToolResult(content=[TextContent(type="text", text=status_text)])

        # Generic handler for other tools
        # Note: This is a simplified example. You might want more specific handlers.
        endpoint_map = {
            "balance_detail": "/core/balance/accumulated/{project_id}",
            "billing_daily_cost": "/core/billing/v2/daily-cost/{project_id}",
            "billing_monthly_cost": "/core/billing/monthly-cost/total-billed/{project_id}",
            "billing_history": ("/core/billing/v2/history", "POST"),
            "k8s_pods": "/core/kubernetes/{project_id}/{namespace}/pods",
            "k8s_deployments": "/core/kubernetes/{project_id}/{namespace}/deployments",
            "k8s_services": "/core/kubernetes/{project_id}/{namespace}/services",
            "k8s_configmaps": "/core/kubernetes/{project_id}/{namespace}/configmaps",
            "k8s_secrets": "/core/kubernetes/{project_id}/{namespace}/secrets",
            "project_list": "/core/user/organization/projects/byOrg",
            "project_detail": "/core/user/project/detail/{project_id}",
            "org_detail": "/core/user/organization",
            "org_members": "/core/user/organization/member",
            "profile_detail": "/core/user/profile",
            "vm_list": "/core/virtual-machine/{project_id}",
            "vm_detail": "/core/virtual-machine/{project_id}/{vm_id}",
            "registry_list": "/core/dekaregistry/v2/{project_id}",
            "registry_repositories": "/core/dekaregistry/v2/repository/{registry_id}",
            "notebook_list": "/core/deka-notebook",
            "notebook_create": ("/core/deka-notebook", "POST"),
            "voucher_list": "/core/voucher",
            "voucher_apply": ("/core/voucher/apply", "POST"),
            "audit_logs": ("/core/auditlog", "POST"),
            "token_list": "/core/cldkctl/token",
            "token_create": ("/core/cldkctl/token", "POST"),
            "token_delete": ("/core/cldkctl/token/{token_id}", "DELETE"),
        }

        if name in endpoint_map:
            mapping = endpoint_map[name]
            method = "GET"
            if isinstance(mapping, tuple):
                endpoint_template, method = mapping
            else:
                endpoint_template = mapping
            
            # Add namespace default if not provided for k8s tools
            if name.startswith("k8s_") and "namespace" not in arguments:
                arguments["namespace"] = "default"

            endpoint = endpoint_template.format(**arguments)
            
            # Separate path variables from body/query params
            body_params = {k: v for k, v in arguments.items() if f"{{{k}}}" not in endpoint_template}

            data = make_authenticated_request(method, endpoint, data=body_params if method in ["POST", "PUT"] else None, params=body_params if method == "GET" else None)
            return CallToolResult(content=[TextContent(type="text", text=format_response(data))])

        else:
            return CallToolResult(content=[TextContent(type="text", text=f"Unknown tool: {name}")])

    except Exception as e:
        print(f"Error calling tool {name}: {e}", file=sys.stderr)
        return CallToolResult(content=[TextContent(type="text", text=f"❌ Error: {str(e)}")])


async def main():
    """Main function."""
    print("Initializing server...", file=sys.stderr)
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="cldkctl",
                server_version="0.1.20",
                capabilities=server.get_capabilities(),
            ),
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server shutting down.", file=sys.stderr)