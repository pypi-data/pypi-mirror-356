from mcp.server.fastmcp import FastMCP
import mcp.types as types
import os
import requests
import sys
from .auth import SessionTokenCache

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

def call_api(method, endpoint, path_params=None, query_params=None, body=None):
    url = BASE_URL + endpoint
    if path_params:
        for k, v in path_params.items():
            url = url.replace(f":{k}", str(v))
    headers = {"Authorization": f"Bearer {TOKEN}"}
    if method in ("POST", "PUT", "PATCH"):
        resp = requests.request(method, url, headers=headers, json=body)
    else:
        resp = requests.request(method, url, headers=headers, params=query_params)
    try:
        resp.raise_for_status()
        return resp.text
    except Exception as e:
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

# --- Token initialization ---
RAW_TOKEN = os.environ.get("CLDKCTL_TOKEN")
TOKEN = RAW_TOKEN

if TOKEN and TOKEN.startswith("cldkctl_"):
    session_token = SessionTokenCache.get_token(TOKEN)
    if session_token:
        TOKEN = session_token
    else:
        print("Fatal error: Could not obtain session token from login token.", file=sys.stderr)
        sys.exit(1)