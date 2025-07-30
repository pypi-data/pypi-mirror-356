# MCP cldkctl Server

This is a Model Context Protocol (MCP) server that provides integration with the Cloudeka CLI (cldkctl) for use in AI assistants like Claude Desktop and Cursor.

## Features

The MCP server exposes the following cldkctl commands as tools:

- **Authentication**: Login and token management
- **Balance**: View project balances
- **Billing**: View billing details
- **Kubernetes**: Manage Kubernetes resources (pods, deployments, services, etc.)
- **Organization**: Manage organization details and members
- **Profile**: View and manage user profile
- **Project**: View and manage projects
- **Registry**: Manage container registry
- **VMs**: Manage virtual machines
- **Voucher**: Manage vouchers and credits
- **Notebook**: Manage notebooks
- **Audit Logs**: View activity logs

## Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager
- [cldkctl](https://github.com/your-repo/cldkctl) CLI tool installed and in PATH

## Installation

### Quick Install

```bash
# Clone the repository
git clone <repository-url>
cd mcp_cldkctl

# Run the installation script
# On Windows:
.\install.ps1

# On Unix/Linux/macOS:
./install.sh
```

### Manual Installation

```bash
# Clone the repository
git clone <repository-url>
cd mcp_cldkctl

# Install dependencies using uv
uv sync

# Install the package
uv pip install -e .
```

## Usage

### Running the MCP Server

```bash
# Run with stdio transport (default)
mcp-cldkctl

# Run with SSE transport
mcp-cldkctl --transport sse --port 8000

# Specify custom cldkctl path
mcp-cldkctl --cldkctl-path /path/to/cldkctl
```

### Configuration

The server will use the same configuration as your cldkctl CLI. Make sure you have:

1. Authenticated with `cldkctl auth`
2. Set up your default project, organization, and other preferences
3. The cldkctl binary available in your PATH

### Integration with Cursor

Add this to your Cursor MCP configuration:

```json
{
  "mcpServers": {
    "cldkctl": {
      "command": "mcp-cldkctl",
      "args": []
    }
  }
}
```

### Integration with Claude Desktop

Add this to your Claude Desktop MCP configuration:

```json
{
  "mcpServers": {
    "cldkctl": {
      "command": "mcp-cldkctl",
      "args": []
    }
  }
}
```

## Testing

Run the test script to verify your installation:

```bash
python test_server.py
```

This will:
- Check if cldkctl is available
- Test basic command execution
- Show you the Cursor configuration

## Available Tools

### Authentication
- `auth`: Authenticate with Cloudeka service using token

### Balance & Billing
- `balance`: View balance for each project
- `billing`: View project billing details

### Kubernetes Management
- `kubernetes`: Manage Kubernetes resources (pods, deployments, services, etc.)

### Organization & Project Management
- `organization`: Manage organization details, members, and roles
- `project`: View and manage your projects

### Infrastructure Management
- `vm`: Manage virtual machines (VMs)
- `registry`: Manage your container registry
- `notebook`: Manage notebooks

### User Management
- `profile`: View and manage your profile information
- `token`: View and manage your Cloudeka authentication tokens

### Financial Management
- `voucher`: Manage project vouchers and credit balances

### Monitoring
- `logs`: View and manage activity logs in the organization's cloud

## Examples

See [examples/usage_examples.md](examples/usage_examples.md) for detailed usage examples.

## Development

```bash
# Install development dependencies
uv sync --group dev

# Run tests
uv run pytest

# Format code
uv run ruff format .

# Lint code
uv run ruff check .
```

## Troubleshooting

### cldkctl not found
Make sure cldkctl is installed and available in your PATH. You can specify a custom path using the `--cldkctl-path` option.

### Authentication errors
Ensure you're authenticated with cldkctl first:
```bash
cldkctl auth your-token
```

### Permission errors
Make sure you have the necessary permissions to execute cldkctl commands and access the required resources.

### Connection issues
Check your network connection and ensure you can reach the Cloudeka API endpoints.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License

## Support

For issues and questions:
- Check the [troubleshooting section](#troubleshooting)
- Review the [usage examples](examples/usage_examples.md)
- Open an issue on the repository 