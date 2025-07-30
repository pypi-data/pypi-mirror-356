# cldkctl MCP Server

cldkctl is a command line interface to interact with Cloudeka service, now fully available as an MCP server for automation and integration.

## Setup

### 1. Install Requirements

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

You must set the following environment variables before running the client:

- `CLDKCTL_TOKEN`: **(Required)** Your Cloudeka API token. Obtain this from your Cloudeka dashboard or admin.
- `CLDKCTL_BASE_URL`: *(Optional, default: https://ai.cloudeka.id)* The base URL for the API.
- `CLDKCTL_DEFAULT_PROJECT_ID`: *(Optional)* The default project ID to use for project-specific actions. If not set, the client will attempt to fetch and use your first available project automatically.

Example (Linux/macOS):
```bash
export CLDKCTL_TOKEN="cldkctl_xxx..."
export CLDKCTL_BASE_URL="https://ai.cloudeka.id"
# Optionally set default project ID
export CLDKCTL_DEFAULT_PROJECT_ID="your_project_id"
```

Example (Windows CMD):
```cmd
set CLDKCTL_TOKEN=cldkctl_xxx...
set CLDKCTL_BASE_URL=https://ai.cloudeka.id
set CLDKCTL_DEFAULT_PROJECT_ID=your_project_id
```

### 3. Obtaining Your Project ID

If you do not know your project ID, you can list your projects using the client:

```python
from mcp_cldkctl.server import project
print(project("list"))
```

Copy the desired project ID and set it as `CLDKCTL_DEFAULT_PROJECT_ID` for convenience.

**Automatic Project ID:**
If `CLDKCTL_DEFAULT_PROJECT_ID` is not set, the client will automatically fetch your projects and use the first one found.

## Example Usage

```python
from mcp_cldkctl.server import project, billing, vm

# List projects
print(project("list"))

# Get project details (uses default project if not provided)
print(project("detail"))

# Get daily cost for default project
print(billing("daily_cost"))

# List all VMs
print(vm("list"))
```

## Authorization

Your API token is required for all requests. Make sure `CLDKCTL_TOKEN` is set in your environment. If you see 401 errors, double-check your token and its validity.

## Troubleshooting
- **401 Unauthorized**: Check your `CLDKCTL_TOKEN` value and expiry.
- **Project ID errors**: Ensure you have access to at least one project. The client will attempt to fetch and use your first project if no default is set.

## License
MIT

## Usage

1. **Install:**
   ```sh
   pip install mcp-cldkctl
   # or build and install locally
   ```

2. **Set your token:**
   ```sh
   export CLDKCTL_TOKEN=your_token
   ```

3. **Run with uvx or python:**
   ```sh
   uvx mcp-cldkctl
   # or
   python -m mcp_cldkctl
   ```

4. **Integrate in Cursor/Claude Desktop:**
   ```json
    {
    "mcpServers": {
        "cldkctl": {
        "command": "uvx",
        "args": ["mcp_cldkctl"],
        "env": {
            "CLDKCTL_TOKEN": "YOUR CLDKCTL TOKEN HERE",
            "CLDKCTL_BASE_URL": "https://ai.cloudeka.id"
            // Optionally:
            // "CLDKCTL_DEFAULT_PROJECT_ID": "your_project_id"
        }
        }
    }
    }

   ```

## Tools

- `project`: Project management (list, detail, update, delete, ...)
- `billing`: Billing queries
- `vm`: Virtual machine management
- `registry`: Container registry management
- `notebook`: Notebook management
- `organization`: Organization management

Each tool has an `action` argument and other relevant parameters.

## Requirements

- Python 3.10+
- [mcp](https://pypi.org/project/mcp/) (`pip install mcp[cli]`)
- Your Cloudeka token

## Example Claude Desktop Configuration

When you connect, Claude Desktop will use the token you provide in the environment variable `CLDKCTL_TOKEN`.

---

For more, see [PyPI MCP docs](https://pypi.org/project/mcp/).

## Usage

You can use the MCP server to call any of the following tools, which map directly to the Cloudeka API endpoints:

### Available Commands

- **auth**: Log in to the Cloudeka service using your token (login token, e.g. `cldkctl_...`).
  - Example: `auth(login_token="cldkctl_...")`
- **balance**: View the balance for each project.
  - Example: `balance(project_id="your_project_id")`
- **billing**: View project billing details (daily cost, monthly cost, summary, etc.).
  - Example: `billing(action="daily_cost", project_id="your_project_id")`
- **kubernetes**: Manage Kubernetes resources (pods, deployments, services, etc.).
  - Example: `kubernetes(action="get", resource="pods")`
- **logs**: View and manage activity logs in the organization's cloud.
  - Example: `logs()`
- **notebook**: Manage Notebooks (list, create, delete, update, start, stop, images).
  - Example: `notebook(action="list")`
- **organization**: Manage organization details, members, and roles.
  - Example: `organization(action="detail")`
- **profile**: View and manage your profile information.
  - Example: `profile(action="detail")`
- **project**: View and manage your projects (list, detail, update, delete).
  - Example: `project(action="list")`
- **registry**: Manage your container registry (list, detail, create, update, delete).
  - Example: `registry(action="list")`
- **token**: View and manage your Cloudeka authentication tokens (list, create, update, delete, regenerate).
  - Example: `token(action="list")`
- **vm**: Manage virtual machines (VMs) (list, detail, create, delete, reboot, turn_on, turn_off).
  - Example: `vm(action="list")`
- **voucher**: Manage project vouchers and credit balances (claim, claimed_list, trial_claimed_list).
  - Example: `voucher(action="claimed_list")`
- **help**: Show this help message.
  - Example: `help()`

### Flags

- `-U, --base-url string`            Base URL for API requests
- `-N, --default-namespace string`   Set a default namespace (default "default")
- `-P, --default-project string`     Set a default project ID to avoid repeated entries
- `-R, --default-registry string`    Set a default registry
- `--editor string`                  Set a default editor (default "vim")
- `-h, --help`                       help for cldkctl
- `--max-retries int`                Maximum number of retries for HTTP requests (default 3)
- `-O, --organization string`        Set an organization
- `-t, --toggle`                     Help message for toggle
- `--version`                        Version information

## Authentication

Before using most commands, you must authenticate using your login token:

```
auth(login_token="cldkctl_...")
```

This will exchange your login token for a JWT and cache it for future requests. The MCP server will automatically re-login if your token expires.

## Full Endpoint Coverage

All Cloudeka API endpoints available in the Go CLI are now accessible as MCP tools. See the docstrings for each tool for detailed usage and parameters.

## Example

```
project(action="list")
balance(project_id="your_project_id")
kubernetes(action="get", resource="pods")
```

## Help

Call `help()` for a summary of all commands and usage. 