# mcp-cldkctl

This MCP server exposes Cloudeka endpoints as tools for LLMs and automation, using the official [MCP Python SDK](https://pypi.org/project/mcp/).

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
         "args": ["mcp-cldkctl"],
         "env": {
           "CLDKCTL_TOKEN": "[YOUR CLDKCTL TOKEN HERE]"
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