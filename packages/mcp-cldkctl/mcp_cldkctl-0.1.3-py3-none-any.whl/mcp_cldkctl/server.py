import os
import mcp.types as types
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import requests

# Complete list of all endpoints from routes.go
ENDPOINTS = [
    ("Login", "POST", "/core/user/login"),
    ("ProfileDetail", "GET", "/core/user/profile"),
    ("UpdateProfile", "PUT", "/core/user/organization/profile/member/:user_id"),
    ("ChangePassword", "POST", "/core/user/change-password"),
    ("ProjectList", "GET", "/core/user/organization/projects/byOrg"),
    ("ProjectDetail", "GET", "/core/user/project/detail/:project_id"),
    ("UpdateProject", "PUT", "/core/user/projects/:project_id"),
    ("CheckBeforeDeleteProject", "DELETE", "/core/user/checking/projects/:project_id"),
    ("DeleteProject", "DELETE", "/core/user/projects/:project_id"),
    ("ProjectRQuotaPost", "GET", "/mid/billing/projectdekagpu/quota/:project_id"),
    ("ProjectRQuotaPre", "GET", "/mid/billing/projectflavorgpu/project/:project_id"),
    ("BalanceDetail", "GET", "/core/balance/accumulated/:project_id"),
    ("PaymentHistory", "GET", "/core/payment/history"),
    ("BillingDailyCost", "GET", "/core/billing/v2/daily-cost/:project_id"),
    ("BillingMonthlyCostTotalBilled", "GET", "/core/billing/monthly-cost/total-billed/:project_id"),
    ("BillingMonthlyCostHistory", "POST", "/core/billing/monthly-cost/history"),
    ("BillingMonthlyCostHistoryDebit", "POST", "/core/billing/monthly-cost/history-debit"),
    ("BillingMonthlyCostByType", "POST", "/core/billing/v2/monthly-cost/by-type"),
    ("BillingMonthlyCostByTypeDetail", "POST", "/core/billing/v2/monthly-cost/by-type/detail"),
    ("BillingHistoryDetail", "POST", "/core/billing/v2/history"),
    ("BillingInvoiceSME", "GET", "/core/balance/history/invoice"),
    ("BillingInvoiceSMEDetail", "GET", "/core/balance/history/invoice/detail/:invoice_id"),
    ("BillingInvoiceEnterprise", "GET", "/core/billing/invoice/:project_id"),
    ("BillingInvoiceEnterpriseDetail", "GET", "/core/billing/v2/invoice/detail/:invoice_id"),
    ("BillingSummary", "GET", "/core/billing/:organization_id/:project_id/summary/monthly"),
    ("BillingSummaryDetail", "GET", "/core/billing/v2/summary/monthly/:summary_id"),
    ("OrgDetail", "GET", "/core/user/organization"),
    ("OrgEdit", "PUT", "/core/user/organization/edit/:organization_id"),
    ("OrgActiveSalesList", "GET", "/core/user/sales/active"),
    ("OrgMemberList", "GET", "/core/user/organization/member"),
    ("OrgMemberAdd", "POST", "/core/user/organization/member"),
    ("OrgMemberEdit", "PUT", "/core/user/organization/member/:user_id"),
    ("OrgMemberDelete", "DELETE", "/core/user/organization/member/:user_id"),
    ("OrgMemberActivate", "PUT", "/core/user/manageuser/active/:user_id"),
    ("OrgMemberDeactivate", "PUT", "/core/user/manageuser/deactive/:user_id"),
    ("OrgMemberResendInvitation", "POST", "/core/superadmin/manageuser/resend-verified/:user_id"),
    ("OrgRoleList", "GET", "/core/user/organization/role"),
    ("OrgRoleDetail", "GET", "/core/user/organization/role/:role_id"),
    ("OrgRoleEdit", "PUT", "/core/user/organization/role/:role_id"),
    ("OrgRoleDelete", "DELETE", "/core/user/organization/role/:role_id"),
    ("OrgRoleAdd", "POST", "/core/user/organization/role"),
    ("VoucherClaim", "POST", "/core/user/voucher-credit/claim"),
    ("VoucherClaimedList", "GET", "/core/user/voucher-credit/claimed"),
    ("VoucherTrialClaimedList", "GET", "/core/user/voucher/claimed"),
    ("AuditLog", "GET", "/core/api/v1.1/user/activity/sp/get-auditlog"),
    ("KubeDashboard", "GET", "/core/user/projects/:project_id/vcluster/dashboard"),
    ("Kubeconfig", "GET", "/core/user/projects/:project_id/vcluster/kubeconfig"),
    ("GetPod", "GET", "/core/pods"),
    ("CreatePod", "POST", "/core/pods"),
    ("EditPod", "PUT", "/core/pods/:project_id/:namespace/:name"),
    ("DeletePod", "DELETE", "/core/pods/:project_id/:namespace/:name"),
    ("ConsolePod", "GET", "/core/pods/console/:token"),
    ("ConsoleTokenPod", "POST", "/core/pods/console"),
    ("GetDeployment", "GET", "/core/deployment"),
    ("CreateDeployment", "POST", "/core/deployment"),
    ("EditDeployment", "PUT", "/core/deployment/:project_id/:namespace/:name"),
    ("DeleteDeployment", "DELETE", "/core/deployment/:project_id/:namespace/:name"),
    ("GetDaemonset", "GET", "/core/daemonset"),
    ("CreateDaemonset", "POST", "/core/daemonset"),
    ("EditDaemonset", "PUT", "/core/daemonset/:project_id/:namespace/:name"),
    ("DeleteDaemonset", "DELETE", "/core/daemonset/:project_id/:namespace/:name"),
    ("GetStatefulset", "GET", "/core/statefulsets"),
    ("CreateStatefulset", "POST", "/core/statefulsets"),
    ("EditStatefulset", "PUT", "/core/statefulsets/:project_id/:namespace/:name"),
    ("DeleteStatefulset", "DELETE", "/core/statefulsets/:project_id/:namespace/:name"),
    ("GetService", "GET", "/core/kubernetes/services"),
    ("CreateService", "POST", "/core/kubernetes/services"),
    ("EditService", "PUT", "/core/kubernetes/services/:project_id/:namespace/:name"),
    ("DeleteService", "DELETE", "/core/kubernetes/services/:project_id/:namespace/:name"),
    ("GetPersistentVolume", "GET", "/core/kubernetes/pv"),
    ("CreatePersistentVolume", "POST", "/core/kubernetes/pv"),
    ("EditPersistentVolume", "PUT", "/core/kubernetes/pv/:project_id/:name"),
    ("DeletePersistentVolume", "DELETE", "/core/kubernetes/pv/:project_id/:name"),
    ("GetPVC", "GET", "/core/kubernetes/pvc"),
    ("CreatePVC", "POST", "/core/kubernetes/pvc"),
    ("EditPVC", "PUT", "/core/kubernetes/pvc/:project_id/:namespace/:name"),
    ("DeletePVC", "DELETE", "/core/kubernetes/pvc/:project_id/:namespace/:name"),
    ("GetDataVolume", "GET", "/core/datavolume"),
    ("CreateDataVolume", "POST", "/core/datavolume"),
    ("EditDataVolume", "PUT", "/core/datavolume/:project_id/:namespace/:name"),
    ("DeleteDataVolume", "DELETE", "/core/datavolume/:project_id/:namespace/:name"),
    ("GetResourceV1", "GET", "/core/kubernetes/:resource"),
    ("CreateResourceV1", "POST", "/core/kubernetes/:resource"),
    ("EditResourceV1", "PATCH", "/core/kubernetes/:resource/:project_id/:namespace/:name"),
    ("DeleteResourceV1", "DELETE", "/core/kubernetes/:resource/:project_id/:namespace/:name"),
    ("GetCustomResources", "GET", "/core/kubernetes/apiresources/:project_id"),
    ("GetCRD", "GET", "/core/kubernetes/resource/:project_id"),
    ("CreateCRD", "POST", "/core/kubernetes/resource"),
    ("EditCRD", "PATCH", "/core/kubernetes/resource/:project_id/:name"),
    ("DeleteCRD", "DELETE", "/core/kubernetes/resource/:project_id/:name"),
    ("GetNamespace", "GET", "/core/user/projects/:project_id/vcluster/namespaces"),
    ("GetImageOS", "GET", "/core/cluster-image-os"),
    ("GetVmFlavorType", "GET", "/core/virtual-machine/flavor_type"),
    ("GetVmGPU", "GET", "/core/virtual-machine/gpu/:project_id"),
    ("GetVmStorageClass", "GET", "/core/virtual-machine/storage-class/:project_id"),
    ("GetVmFlavor", "GET", "/core/virtual-machine/flavor/:flavorType_id"),
    ("CreateVm", "POST", "/core/virtual-machine"),
    ("CreateVmYaml", "POST", "/core/virtual-machine/yaml"),
    ("GetVm", "GET", "/core/virtual-machine/list/all"),
    ("VmDetail", "POST", "/core/virtual-machine/detail-vm"),
    ("EditVmYaml", "PUT", "/core/virtual-machine/yaml/:project_id/:namespace/:name"),
    ("DeleteVm", "POST", "/core/virtual-machine/delete"),
    ("RebootVm", "POST", "/core/virtual-machine/reboot"),
    ("TurnOffVm", "POST", "/core/virtual-machine/turn-off/vm"),
    ("TurnOnVm", "POST", "/core/virtual-machine/turn-on/vm"),
    ("RegistryQuota", "GET", "/core/dekaregistry/v2/project/quota/:project_id"),
    ("RegistryList", "GET", "/core/dekaregistry/v2/registry"),
    ("RegistryOverview", "GET", "/core/dekaregistry/v2/registry/:registry_id/overview"),
    ("RegistryCert", "GET", "/core/dekaregistry/v1/registry/downloadcrt"),
    ("RegistryCreate", "POST", "/core/dekaregistry/v2/registry"),
    ("RegistryUpdate", "PUT", "/core/dekaregistry/v2/registry/:registry_id"),
    ("RegistryDetail", "GET", "/core/dekaregistry/v2/registry/:registry_id"),
    ("RegistryLogs", "GET", "/core/dekaregistry/v2/registry/:registry_id/logs"),
    ("RegistryLabels", "GET", "/core/dekaregistry/v1/registry/lislabels/:organization_id/:user_id/:project_id/:registry_id"),
    ("RegistryLabelsUpdate", "PUT", "/core/dekaregistry/v1/registry/updatelabels/:organization_id/:user_id/:project_id/:registry_id"),
    ("RegistryLabelsCreate", "POST", "/core/dekaregistry/v1/registry/createlabels/:organization_id/:user_id/:project_id/:registry_id"),
    ("RegistryLabelsDelete", "DELETE", "/core/dekaregistry/v1/registry/deletelabels/:organization_id/:user_id/:project_id/:labels_id/:registry_id"),
    ("RegistryTagList", "GET", "/core/dekaregistry/v2/tag/:registry_id"),
    ("RegistryTagCreate", "POST", "/core/dekaregistry/v2/tag/:registry_id"),
    ("RegistryTagUpdate", "PUT", "/core/dekaregistry/v2/tag/detail/:tag_id"),
    ("RegistryTagDelete", "DELETE", "/core/dekaregistry/v2/tag/detail/:tag_id"),
    ("RegistryTagDisable", "POST", "/core/dekaregistry/v2/tag/detail/:tag_id/disable"),
    ("RegistryTagEnable", "POST", "/core/dekaregistry/v2/tag/detail/:tag_id/enable"),
    ("RegistryMemberList", "GET", "/core/dekaregistry/v2/member/:registry_id"),
    ("RegistryAvailableMember", "GET", "/core/dekaregistry/v2/project/member/:project_id"),
    ("RegistryShowPassword", "POST", "/core/dekaregistry/v2/user/password/show"),
    ("RegistryMemberAdd", "POST", "/core/dekaregistry/v2/member/:registry_id"),
    ("RegistryMemberDelete", "DELETE", "/core/dekaregistry/v2/member/:registry_id/detail/:member_id"),
    ("RegistryRepositoryList", "GET", "/core/dekaregistry/v2/repository"),
    ("RegistryArtifactList", "GET", "/core/dekaregistry/v2/artifact"),
    ("RegistryArtifactDetail", "GET", "/core/dekaregistry/v2/artifact/:artifact_id"),
    ("RegistryArtifactAddLabel", "PATCH", "/core/dekaregistry/v2/artifact/:artifact_id/assign-label/:label_id"),
    ("RegistryArtifactRemoveLabel", "PATCH", "/core/dekaregistry/v2/artifact/:artifact_id/unassign-label/:label_id"),
    ("RegistryArtifactScan", "POST", "/core/dekaregistry/v2/artifact/:artifact_id/scan"),
    ("RegistryArtifactStopScan", "POST", "/core/dekaregistry/v2/artifact/:artifact_id/stop-scan"),
    ("RegistryArtifactTags", "GET", "/core/dekaregistry/v2/artifact/:artifact_id/tag"),
    ("RegistryArtifactDeleteTag", "DELETE", "/core/dekaregistry/v2/artifact/:artifact_id/tag/:tag"),
    ("RegistryArtifactAddTag", "POST", "/core/dekaregistry/v2/artifact/:artifact_id/tag/:tag"),
    ("NotebookList", "GET", "/core/deka-notebook"),
    ("NotebookCreate", "POST", "/core/deka-notebook"),
    ("NotebookDelete", "POST", "/core/deka-notebook/delete"),
    ("NotebookUpdate", "PUT", "/core/deka-notebook/yaml"),
    ("NotebookStart", "POST", "/core/deka-notebook/start"),
    ("NotebookStop", "POST", "/core/deka-notebook/stop"),
    ("NotebookImages", "GET", "/core/deka-notebook/images"),
    ("CldkctlAuth", "POST", "/core/cldkctl/auth"),
    ("CldkctlCreateToken", "POST", "/core/cldkctl/token"),
    ("CldkctlTokenList", "GET", "/core/cldkctl/token"),
    ("CldkctlUpdateToken", "PUT", "/core/cldkctl/token/:token_id"),
    ("CldkctlDeleteToken", "DELETE", "/core/cldkctl/token/:token_id"),
    ("CldkctlRegenerateToken", "POST", "/core/cldkctl/token/regenerate/:token_id"),
    ("SuperadminProjectList", "GET", "/core/superadmin/list/manageorgproject"),
    ("SuperadminOrgDetail", "GET", "/core/superadmin/manageorg/:organization_id"),
    ("SuperadminBalanceDetail", "GET", "/core/superadmin/balance/accumulated/:organization_id/:project_id"),
    ("SuperadminBillingInvoiceSME", "GET", "/core/superadmin/balance/history/invoice/:organization_id"),
    ("SuperadminBillingInvoiceEnterprise", "GET", "/core/superadmin/invoice/:organization_id/:project_id"),
]

BASE_URL = os.environ.get("CLDKCTL_BASE_URL", "https://api.cloudeka.id")

def get_tool_list():
    return [
        types.Tool(
            name=name,
            title=f"{name} [{method}]",
            description=f"{method} {endpoint}",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ) for (name, method, endpoint) in ENDPOINTS
    ]

server = Server("mcp-cldkctl")

def call_api(method, endpoint, token, path_params=None, query_params=None, body=None):
    url = BASE_URL + endpoint
    if path_params:
        for k, v in path_params.items():
            url = url.replace(f":{k}", str(v))
    headers = {"Authorization": f"Bearer {token}"}
    if method in ("POST", "PUT", "PATCH"):
        resp = requests.request(method, url, headers=headers, json=body)
    else:
        resp = requests.request(method, url, headers=headers, params=query_params)
    try:
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        return f"Error: {e}\n{resp.text}"

# --- Project Tool ---
@server.tool(
    name="project",
    title="Project Management",
    description="Manage and query projects.",
    inputSchema={
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["list", "detail", "update", "delete", "quota_post", "quota_pre"]},
            "project_id": {"type": "string"},
            "body": {"type": "object"}
        },
        "required": ["action"]
    },
)
async def project_tool(action: str, project_id: str = None, body: dict = None) -> list[types.ContentBlock]:
    token = os.environ.get("CLDKCTL_TOKEN", "")
    if action == "list":
        output = call_api("GET", "/core/user/organization/projects/byOrg", token)
    elif action == "detail" and project_id:
        output = call_api("GET", f"/core/user/project/detail/{project_id}", token)
    elif action == "update" and project_id and body:
        output = call_api("PUT", f"/core/user/projects/{project_id}", token, body=body)
    elif action == "delete" and project_id:
        output = call_api("DELETE", f"/core/user/projects/{project_id}", token)
    elif action == "quota_post" and project_id:
        output = call_api("GET", f"/mid/billing/projectdekagpu/quota/{project_id}", token)
    elif action == "quota_pre" and project_id:
        output = call_api("GET", f"/mid/billing/projectflavorgpu/project/{project_id}", token)
    else:
        output = "Invalid action or missing parameters."
    return [types.TextContent(type="text", text=output)]

# --- Billing Tool ---
@server.tool(
    name="billing",
    title="Billing Management",
    description="Query billing information.",
    inputSchema={
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["daily_cost", "monthly_cost_total_billed", "monthly_cost_history", "summary", "summary_detail"]},
            "project_id": {"type": "string"},
            "summary_id": {"type": "string"},
            "body": {"type": "object"}
        },
        "required": ["action"]
    },
)
async def billing_tool(action: str, project_id: str = None, summary_id: str = None, body: dict = None) -> list[types.ContentBlock]:
    token = os.environ.get("CLDKCTL_TOKEN", "")
    if action == "daily_cost" and project_id:
        output = call_api("GET", f"/core/billing/v2/daily-cost/{project_id}", token)
    elif action == "monthly_cost_total_billed" and project_id:
        output = call_api("GET", f"/core/billing/monthly-cost/total-billed/{project_id}", token)
    elif action == "monthly_cost_history" and body:
        output = call_api("POST", "/core/billing/monthly-cost/history", token, body=body)
    elif action == "summary" and project_id:
        output = call_api("GET", f"/core/billing/:organization_id/{project_id}/summary/monthly", token)
    elif action == "summary_detail" and summary_id:
        output = call_api("GET", f"/core/billing/v2/summary/monthly/{summary_id}", token)
    else:
        output = "Invalid action or missing parameters."
    return [types.TextContent(type="text", text=output)]

# --- VM Tool ---
@server.tool(
    name="vm",
    title="Virtual Machine Management",
    description="Manage and query virtual machines.",
    inputSchema={
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["list", "detail", "create", "delete", "reboot", "turn_on", "turn_off"]},
            "project_id": {"type": "string"},
            "body": {"type": "object"}
        },
        "required": ["action"]
    },
)
async def vm_tool(action: str, project_id: str = None, body: dict = None) -> list[types.ContentBlock]:
    token = os.environ.get("CLDKCTL_TOKEN", "")
    if action == "list":
        output = call_api("GET", "/core/virtual-machine/list/all", token)
    elif action == "detail" and body:
        output = call_api("POST", "/core/virtual-machine/detail-vm", token, body=body)
    elif action == "create" and body:
        output = call_api("POST", "/core/virtual-machine", token, body=body)
    elif action == "delete" and body:
        output = call_api("POST", "/core/virtual-machine/delete", token, body=body)
    elif action == "reboot" and body:
        output = call_api("POST", "/core/virtual-machine/reboot", token, body=body)
    elif action == "turn_on" and body:
        output = call_api("POST", "/core/virtual-machine/turn-on/vm", token, body=body)
    elif action == "turn_off" and body:
        output = call_api("POST", "/core/virtual-machine/turn-off/vm", token, body=body)
    else:
        output = "Invalid action or missing parameters."
    return [types.TextContent(type="text", text=output)]

# --- Registry Tool ---
@server.tool(
    name="registry",
    title="Registry Management",
    description="Manage and query container registries.",
    inputSchema={
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["list", "detail", "create", "update", "delete"]},
            "registry_id": {"type": "string"},
            "body": {"type": "object"}
        },
        "required": ["action"]
    },
)
async def registry_tool(action: str, registry_id: str = None, body: dict = None) -> list[types.ContentBlock]:
    token = os.environ.get("CLDKCTL_TOKEN", "")
    if action == "list":
        output = call_api("GET", "/core/dekaregistry/v2/registry", token)
    elif action == "detail" and registry_id:
        output = call_api("GET", f"/core/dekaregistry/v2/registry/{registry_id}", token)
    elif action == "create" and body:
        output = call_api("POST", "/core/dekaregistry/v2/registry", token, body=body)
    elif action == "update" and registry_id and body:
        output = call_api("PUT", f"/core/dekaregistry/v2/registry/{registry_id}", token, body=body)
    elif action == "delete" and registry_id:
        output = call_api("DELETE", f"/core/dekaregistry/v2/registry/{registry_id}", token)
    else:
        output = "Invalid action or missing parameters."
    return [types.TextContent(type="text", text=output)]

# --- Notebook Tool ---
@server.tool(
    name="notebook",
    title="Notebook Management",
    description="Manage and query notebooks.",
    inputSchema={
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["list", "create", "delete", "update", "start", "stop", "images"]},
            "body": {"type": "object"}
        },
        "required": ["action"]
    },
)
async def notebook_tool(action: str, body: dict = None) -> list[types.ContentBlock]:
    token = os.environ.get("CLDKCTL_TOKEN", "")
    if action == "list":
        output = call_api("GET", "/core/deka-notebook", token)
    elif action == "create" and body:
        output = call_api("POST", "/core/deka-notebook", token, body=body)
    elif action == "delete" and body:
        output = call_api("POST", "/core/deka-notebook/delete", token, body=body)
    elif action == "update" and body:
        output = call_api("PUT", "/core/deka-notebook/yaml", token, body=body)
    elif action == "start" and body:
        output = call_api("POST", "/core/deka-notebook/start", token, body=body)
    elif action == "stop" and body:
        output = call_api("POST", "/core/deka-notebook/stop", token, body=body)
    elif action == "images":
        output = call_api("GET", "/core/deka-notebook/images", token)
    else:
        output = "Invalid action or missing parameters."
    return [types.TextContent(type="text", text=output)]

# --- Organization Tool ---
@server.tool(
    name="organization",
    title="Organization Management",
    description="Manage and query organizations.",
    inputSchema={
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["detail", "edit", "active_sales_list", "member_list", "member_add", "member_edit", "member_delete"]},
            "organization_id": {"type": "string"},
            "user_id": {"type": "string"},
            "body": {"type": "object"}
        },
        "required": ["action"]
    },
)
async def organization_tool(action: str, organization_id: str = None, user_id: str = None, body: dict = None) -> list[types.ContentBlock]:
    token = os.environ.get("CLDKCTL_TOKEN", "")
    if action == "detail":
        output = call_api("GET", "/core/user/organization", token)
    elif action == "edit" and organization_id and body:
        output = call_api("PUT", f"/core/user/organization/edit/{organization_id}", token, body=body)
    elif action == "active_sales_list":
        output = call_api("GET", "/core/user/sales/active", token)
    elif action == "member_list":
        output = call_api("GET", "/core/user/organization/member", token)
    elif action == "member_add" and body:
        output = call_api("POST", "/core/user/organization/member", token, body=body)
    elif action == "member_edit" and user_id and body:
        output = call_api("PUT", f"/core/user/organization/member/{user_id}", token, body=body)
    elif action == "member_delete" and user_id:
        output = call_api("DELETE", f"/core/user/organization/member/{user_id}", token)
    else:
        output = "Invalid action or missing parameters."
    return [types.TextContent(type="text", text=output)]

# Add more tools for other logical groups as needed...

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-cldkctl",
                server_version="0.1.3",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        ) 