from mcp.server.fastmcp import FastMCP
import mcp.types as types
import os
import requests
import sys
from .auth import SessionTokenCache
import base64
import json
import threading

BASE_URL = os.environ.get("CLDKCTL_BASE_URL", "https://ai.cloudeka.id")
TOKEN = os.environ.get("CLDKCTL_TOKEN")
DEFAULT_PROJECT_ID = os.environ.get("CLDKCTL_DEFAULT_PROJECT_ID")

# Debug: Print token for troubleshooting (remove/comment out in production)
print("[DEBUG] CLDKCTL_TOKEN:", TOKEN)

# Validate token format (basic JWT check: 3 segments separated by '.')
def is_valid_token(token):
    if not token:
        return False
    parts = token.split('.')
    return len(parts) == 3 or token.startswith('cldkctl_')  # Accepts JWT or cldkctl_ prefix

if not is_valid_token(TOKEN):
    print("Fatal error: CLDKCTL_TOKEN environment variable is not set or invalid. Please set it in your Claude Desktop configuration using the 'env' field. Token must be a valid JWT or cldkctl_ token.", file=sys.stderr)
    sys.exit(1)

# --- Auto-fetch default project ID if not set ---
def fetch_first_project_id():
    try:
        resp = requests.get(
            BASE_URL + "/core/user/organization/projects/byOrg",
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        resp.raise_for_status()
        data = resp.json()
        # Try to find the first project ID in the response
        if isinstance(data, dict):
            projects = data.get("data") or data.get("projects") or data.get("result")
        elif isinstance(data, list):
            projects = data
        else:
            projects = None
        if projects and isinstance(projects, list) and len(projects) > 0:
            first_project = projects[0]
            # Try common keys for project ID
            for key in ("id", "project_id", "_id"):
                if key in first_project:
                    return first_project[key]
            # Fallback: return the first value
            return list(first_project.values())[0]
        else:
            print("[WARN] No projects found for this user.")
            return None
    except Exception as e:
        print(f"[ERROR] Could not auto-fetch project ID: {e}")
        return None

if not DEFAULT_PROJECT_ID:
    fetched_id = fetch_first_project_id()
    if fetched_id:
        DEFAULT_PROJECT_ID = fetched_id
        print(f"[INFO] Using auto-fetched default project ID: {DEFAULT_PROJECT_ID}")
    else:
        print("[WARN] No default project ID set and none could be fetched. Some actions may fail.")

mcp = FastMCP("cldkctl")

# --- Token cache (in-memory, could be extended to file-based) ---
class TokenCache:
    _lock = threading.Lock()
    _jwt_token = None
    _login_payload = None  # base64-encoded JSON

    @classmethod
    def set_jwt(cls, token):
        with cls._lock:
            cls._jwt_token = token

    @classmethod
    def get_jwt(cls):
        with cls._lock:
            return cls._jwt_token

    @classmethod
    def set_login_payload(cls, payload):
        with cls._lock:
            cls._login_payload = payload

    @classmethod
    def get_login_payload(cls):
        with cls._lock:
            return cls._login_payload

# --- Auth logic ---
def exchange_login_token_for_jwt(login_token):
    """Exchange a cldkctl_ login token for a JWT via /core/cldkctl/auth."""
    url = BASE_URL + "/core/cldkctl/auth"
    payload = {"token": login_token}
    resp = requests.post(url, json=payload)
    try:
        resp.raise_for_status()
        data = resp.json()
        jwt_token = data.get("data", {}).get("token") or data.get("data", {}).get("Token")
        if not jwt_token:
            raise Exception("No JWT token in response")
        # Save login payload for re-login
        TokenCache.set_login_payload(base64.b64encode(json.dumps(payload).encode()).decode())
        TokenCache.set_jwt(jwt_token)
        return jwt_token
    except Exception as e:
        print(f"[ERROR] Failed to exchange login token: {e}", file=sys.stderr)
        return None

def relogin_with_cached_payload():
    """Re-login using the cached login payload (base64-encoded JSON)."""
    payload_b64 = TokenCache.get_login_payload()
    if not payload_b64:
        print("[ERROR] No cached login payload for re-login.", file=sys.stderr)
        return None
    try:
        payload = json.loads(base64.b64decode(payload_b64).decode())
        url = BASE_URL + "/core/cldkctl/auth"
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()
        jwt_token = data.get("data", {}).get("token") or data.get("data", {}).get("Token")
        if not jwt_token:
            raise Exception("No JWT token in response")
        TokenCache.set_jwt(jwt_token)
        return jwt_token
    except Exception as e:
        print(f"[ERROR] Failed to re-login: {e}", file=sys.stderr)
        return None

def get_valid_token():
    """Get a valid JWT token, re-login if needed."""
    token = TokenCache.get_jwt()
    if token:
        return token
    # Try to re-login
    return relogin_with_cached_payload()

# --- Remove debug prints ---
# (Removed all [DEBUG], [WARN], [ERROR] prints except those to stderr)

# --- MCP tool: auth ---
@mcp.tool()
def auth(login_token: str) -> str:
    """Authenticate with Cloudeka service using a login token (cldkctl_...). Exchanges for a JWT and caches it for future use."""
    jwt_token = exchange_login_token_for_jwt(login_token)
    if jwt_token:
        return "Authentication successful. JWT token obtained and cached."
    else:
        return "Authentication failed. See server logs for details."

# --- Patch call_api to use the new token logic ---
def call_api(method, endpoint, path_params=None, query_params=None, body=None):
    url = BASE_URL + endpoint
    if path_params:
        for k, v in path_params.items():
            url = url.replace(f":{k}", str(v))
    token = get_valid_token()
    if not token:
        return "Error: No valid authentication token. Please run the 'auth' tool with your login token."
    headers = {"Authorization": f"Bearer {token}"}
    if method in ("POST", "PUT", "PATCH"):
        resp = requests.request(method, url, headers=headers, json=body)
    else:
        resp = requests.request(method, url, headers=headers, params=query_params)
    try:
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        # If unauthorized, try re-login once
        if resp.status_code == 401:
            new_token = relogin_with_cached_payload()
            if new_token:
                headers["Authorization"] = f"Bearer {new_token}"
                resp = requests.request(method, url, headers=headers, json=body if method in ("POST", "PUT", "PATCH") else None, params=query_params if method not in ("POST", "PUT", "PATCH") else None)
                try:
                    resp.raise_for_status()
                    return resp.text
                except Exception as e2:
                    return f"Error after re-login: {e2}\n{resp.text}"
        return f"Error: {e}\n{resp.text}"

@mcp.tool()
def project(action: str, project_id: str = None, body: dict = None) -> str:
    """Project management actions. Actions: list, detail, update, delete."""
    if action == "list":
        return call_api("GET", "/core/user/organization/projects/byOrg")
    # Use default project ID if not provided
    if not project_id and DEFAULT_PROJECT_ID:
        project_id = DEFAULT_PROJECT_ID
    if action == "detail" and project_id:
        return call_api("GET", f"/core/user/project/detail/{project_id}")
    elif action == "update" and project_id and body:
        return call_api("PUT", f"/core/user/projects/{project_id}", body=body)
    elif action == "delete" and project_id:
        return call_api("DELETE", f"/core/user/projects/{project_id}")
    else:
        return "Invalid action or missing parameters. Use action: list, detail, update, delete. Provide project_id where required."

@mcp.tool()
def billing(action: str, project_id: str = None, summary_id: str = None, body: dict = None) -> str:
    """Billing management actions. Actions: daily_cost, monthly_cost_total_billed, monthly_cost_history, summary, summary_detail."""
    if not project_id and DEFAULT_PROJECT_ID:
        project_id = DEFAULT_PROJECT_ID
    if action == "daily_cost" and project_id:
        return call_api("GET", f"/core/billing/v2/daily-cost/{project_id}")
    elif action == "monthly_cost_total_billed" and project_id:
        return call_api("GET", f"/core/billing/monthly-cost/total-billed/{project_id}")
    elif action == "monthly_cost_history" and body:
        return call_api("POST", "/core/billing/monthly-cost/history", body=body)
    elif action == "summary" and project_id:
        return call_api("GET", f"/core/billing/:organization_id/{project_id}/summary/monthly")
    elif action == "summary_detail" and summary_id:
        return call_api("GET", f"/core/billing/v2/summary/monthly/{summary_id}")
    else:
        return "Invalid action or missing parameters. Use action: daily_cost, monthly_cost_total_billed, monthly_cost_history, summary, summary_detail. Provide project_id or summary_id where required."

@mcp.tool()
def vm(action: str, project_id: str = None, body: dict = None) -> str:
    """Virtual machine management actions. Actions: list, detail, create, delete, reboot, turn_on, turn_off."""
    if not project_id and DEFAULT_PROJECT_ID:
        project_id = DEFAULT_PROJECT_ID
    if action == "list":
        return call_api("GET", "/core/virtual-machine/list/all")
    elif action == "detail" and body:
        return call_api("POST", "/core/virtual-machine/detail-vm", body=body)
    elif action == "create" and body:
        return call_api("POST", "/core/virtual-machine", body=body)
    elif action == "delete" and body:
        return call_api("POST", "/core/virtual-machine/delete", body=body)
    elif action == "reboot" and body:
        return call_api("POST", "/core/virtual-machine/reboot", body=body)
    elif action == "turn_on" and body:
        return call_api("POST", "/core/virtual-machine/turn-on/vm", body=body)
    elif action == "turn_off" and body:
        return call_api("POST", "/core/virtual-machine/turn-off/vm", body=body)
    else:
        return "Invalid action or missing parameters. Use action: list, detail, create, delete, reboot, turn_on, turn_off. Provide body where required."

@mcp.tool()
def registry(action: str, registry_id: str = None, body: dict = None) -> str:
    """Registry management actions. Actions: list, detail, create, update, delete."""
    if action == "list":
        return call_api("GET", "/core/dekaregistry/v2/registry")
    elif action == "detail" and registry_id:
        return call_api("GET", f"/core/dekaregistry/v2/registry/{registry_id}")
    elif action == "create" and body:
        return call_api("POST", "/core/dekaregistry/v2/registry", body=body)
    elif action == "update" and registry_id and body:
        return call_api("PUT", f"/core/dekaregistry/v2/registry/{registry_id}", body=body)
    elif action == "delete" and registry_id:
        return call_api("DELETE", f"/core/dekaregistry/v2/registry/{registry_id}")
    else:
        return "Invalid action or missing parameters. Use action: list, detail, create, update, delete. Provide registry_id or body where required."

@mcp.tool()
def notebook(action: str, body: dict = None) -> str:
    """Notebook management actions. Actions: list, create, delete, update, start, stop, images."""
    if action == "list":
        return call_api("GET", "/core/deka-notebook")
    elif action == "create" and body:
        return call_api("POST", "/core/deka-notebook", body=body)
    elif action == "delete" and body:
        return call_api("POST", "/core/deka-notebook/delete", body=body)
    elif action == "update" and body:
        return call_api("PUT", "/core/deka-notebook/yaml", body=body)
    elif action == "start" and body:
        return call_api("POST", "/core/deka-notebook/start", body=body)
    elif action == "stop" and body:
        return call_api("POST", "/core/deka-notebook/stop", body=body)
    elif action == "images":
        return call_api("GET", "/core/deka-notebook/images")
    else:
        return "Invalid action or missing parameters. Use action: list, create, delete, update, start, stop, images. Provide body where required."

@mcp.tool()
def organization(action: str, organization_id: str = None, user_id: str = None, body: dict = None) -> str:
    """Organization management actions. Actions: detail, edit, active_sales_list, member_list, member_add, member_edit, member_delete."""
    if action == "detail":
        return call_api("GET", "/core/user/organization")
    elif action == "edit" and organization_id and body:
        return call_api("PUT", f"/core/user/organization/edit/{organization_id}", body=body)
    elif action == "active_sales_list":
        return call_api("GET", "/core/user/sales/active")
    elif action == "member_list":
        return call_api("GET", "/core/user/organization/member")
    elif action == "member_add" and body:
        return call_api("POST", "/core/user/organization/member", body=body)
    elif action == "member_edit" and user_id and body:
        return call_api("PUT", f"/core/user/organization/member/{user_id}", body=body)
    elif action == "member_delete" and user_id:
        return call_api("DELETE", f"/core/user/organization/member/{user_id}")
    else:
        return "Invalid action or missing parameters. Use action: detail, edit, active_sales_list, member_list, member_add, member_edit, member_delete. Provide organization_id, user_id, or body where required."

# =====================
# MCP TOOLS - CLI STRUCTURE
# =====================

@mcp.tool()
def balance(project_id: str = None) -> str:
    """View the balance for a project. If project_id is not provided, uses the default project."""
    if not project_id and DEFAULT_PROJECT_ID:
        project_id = DEFAULT_PROJECT_ID
    if not project_id:
        return "Missing project_id."
    return call_api("GET", f"/core/balance/accumulated/{project_id}")

@mcp.tool()
def profile(action: str = "detail", user_id: str = None, body: dict = None) -> str:
    """View and manage your profile information. Actions: detail, update, change_password."""
    if action == "detail":
        return call_api("GET", "/core/user/profile")
    elif action == "update" and user_id and body:
        return call_api("PUT", f"/core/user/organization/profile/member/{user_id}", body=body)
    elif action == "change_password" and body:
        return call_api("POST", "/core/user/change-password", body=body)
    else:
        return "Invalid action or missing parameters. Use action: detail, update, change_password. Provide user_id/body where required."

@mcp.tool()
def voucher(action: str, body: dict = None) -> str:
    """Manage project vouchers and credit balances. Actions: claim, claimed_list, trial_claimed_list."""
    if action == "claim" and body:
        return call_api("POST", "/core/user/voucher-credit/claim", body=body)
    elif action == "claimed_list":
        return call_api("GET", "/core/user/voucher-credit/claimed")
    elif action == "trial_claimed_list":
        return call_api("GET", "/core/user/voucher/claimed")
    else:
        return "Invalid action or missing parameters. Use action: claim, claimed_list, trial_claimed_list. Provide body where required."

@mcp.tool()
def logs() -> str:
    """View and manage activity logs in the organization's cloud."""
    return call_api("GET", "/core/api/v1.1/user/activity/sp/get-auditlog")

@mcp.tool()
def token(action: str, token_id: str = None, body: dict = None) -> str:
    """View and manage your Cloudeka authentication tokens. Actions: list, create, update, delete, regenerate."""
    if action == "list":
        return call_api("GET", "/core/cldkctl/token")
    elif action == "create" and body:
        return call_api("POST", "/core/cldkctl/token", body=body)
    elif action == "update" and token_id and body:
        return call_api("PUT", f"/core/cldkctl/token/{token_id}", body=body)
    elif action == "delete" and token_id:
        return call_api("DELETE", f"/core/cldkctl/token/{token_id}")
    elif action == "regenerate" and token_id and body:
        return call_api("POST", f"/core/cldkctl/token/regenerate/{token_id}", body=body)
    else:
        return "Invalid action or missing parameters. Use action: list, create, update, delete, regenerate. Provide token_id/body where required."

@mcp.tool()
def kubernetes(action: str, resource: str = None, project_id: str = None, namespace: str = None, name: str = None, body: dict = None) -> str:
    """Manage Kubernetes resources. Actions: get, create, edit, delete, dashboard, kubeconfig, namespace_list. Resource: pods, deployment, daemonset, statefulsets, services, pv, pvc, datavolume, etc."""
    # Example: get pods, create deployment, edit service, delete pvc, etc.
    # For dashboard/kubeconfig/namespace_list, only project_id is needed.
    if action == "dashboard" and project_id:
        return call_api("GET", f"/core/user/projects/{project_id}/vcluster/dashboard")
    elif action == "kubeconfig" and project_id:
        return call_api("GET", f"/core/user/projects/{project_id}/vcluster/kubeconfig")
    elif action == "namespace_list" and project_id:
        return call_api("GET", f"/core/user/projects/{project_id}/vcluster/namespaces")
    elif action in ("get", "create", "edit", "delete") and resource:
        # Map action/resource to endpoint
        base = f"/core/{resource}"
        if action == "get":
            return call_api("GET", base)
        elif action == "create" and body:
            return call_api("POST", base, body=body)
        elif action == "edit" and project_id and namespace and name and body:
            return call_api("PUT", f"{base}/{project_id}/{namespace}/{name}", body=body)
        elif action == "delete" and project_id and namespace and name:
            return call_api("DELETE", f"{base}/{project_id}/{namespace}/{name}")
        else:
            return "Missing parameters for resource action."
    else:
        return "Invalid action or missing parameters. See docstring for usage."

# Add help tool for discoverability
@mcp.tool()
def help() -> str:
    """cldkctl is a command line interface to interact with Cloudeka service.\n\nUsage:\n  cldkctl [flags]\n  cldkctl [command]\n\nAvailable Commands:\n  auth         Log in to the Cloudeka service using your token\n  balance      View the balance for each project\n  billing      View project billing details\n  completion   Generate the autocompletion script for the specified shell\n  help         Help about any command\n  kubernetes   Manage Kubernetes resources\n  logs         View and manage activity logs in the organizations cloud\n  notebook     Manage Notebooks\n  organization Manage organization details, members, and roles\n  profile      View and manage your profile information\n  project      View and manage your projects\n  registry     Manage your container registry\n  token        View and manage your Cloudeka authentication tokens\n  vm           Manage virtual machines (VMs)\n  voucher      Manage project vouchers and credit balances\n\nFlags:\n  -U, --base-url string            Base URL for API requests\n  -N, --default-namespace string   Set a default namespace (default \"default\")\n  -P, --default-project string     Set a default project ID to avoid repeated entries\n  -R, --default-registry string    Set a default registry\n      --editor string              Set a default editor (default \"vim\")\n  -h, --help                       help for cldkctl\n      --max-retries int            Maximum number of retries for HTTP requests (default 3)\n  -O, --organization string        Set an organization\n  -t, --toggle                     Help message for toggle\n      --version                    Version information\n\nUse \"cldkctl [command] --help\" for more information about a command."""
    return help.__doc__