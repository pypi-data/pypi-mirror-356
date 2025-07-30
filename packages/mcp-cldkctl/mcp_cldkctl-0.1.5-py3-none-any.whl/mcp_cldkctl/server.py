from mcp.server.fastmcp import FastMCP
import mcp.types as types
import os
import requests

BASE_URL = os.environ.get("CLDKCTL_BASE_URL", "https://api.cloudeka.id")
TOKEN = os.environ.get("CLDKCTL_TOKEN", "")

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
    """Project management actions."""
    if action == "list":
        return call_api("GET", "/core/user/organization/projects/byOrg")
    elif action == "detail" and project_id:
        return call_api("GET", f"/core/user/project/detail/{project_id}")
    elif action == "update" and project_id and body:
        return call_api("PUT", f"/core/user/projects/{project_id}", body=body)
    elif action == "delete" and project_id:
        return call_api("DELETE", f"/core/user/projects/{project_id}")
    else:
        return "Invalid action or missing parameters."

@mcp.tool()
def billing(action: str, project_id: str = None, summary_id: str = None, body: dict = None) -> str:
    """Billing management actions."""
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
        return "Invalid action or missing parameters."

@mcp.tool()
def vm(action: str, project_id: str = None, body: dict = None) -> str:
    """Virtual machine management actions."""
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
        return "Invalid action or missing parameters."

@mcp.tool()
def registry(action: str, registry_id: str = None, body: dict = None) -> str:
    """Registry management actions."""
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
        return "Invalid action or missing parameters."

@mcp.tool()
def notebook(action: str, body: dict = None) -> str:
    """Notebook management actions."""
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
        return "Invalid action or missing parameters."

@mcp.tool()
def organization(action: str, organization_id: str = None, user_id: str = None, body: dict = None) -> str:
    """Organization management actions."""
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
        return "Invalid action or missing parameters."