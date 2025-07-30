# mcp_cldkctl

This package provides an MCP server that wraps the Cloudeka `cldkctl` CLI, exposing its commands as MCP tools for integration with Model Context Protocol (MCP) clients and Cursor.

## Features
- Exposes all major `cldkctl` commands (auth, balance, billing, kubernetes, logs, notebook, organization, profile, project, registry, token, vm, voucher) as MCP tools.
- Allows programmatic access to Cloudeka services via MCP.
- Shells out to the Go `cldkctl` binary for each command, returning the output as text.

## Usage

Install the package (after building):
```sh
pip install mcp_cldkctl
```

Run the MCP server:
```sh
python -m mcp_cldkctl
```

Or use the script:
```sh
mcp_cldkctl
```

## Authentication

You must provide your Cloudeka token. The server will use this token when invoking the CLI.

## Development
- Requires the `cldkctl` binary to be available in the system PATH or in the same directory as the server.
- See the code for details on how each command is mapped. 