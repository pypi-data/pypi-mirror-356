"""MCP server for Cloudeka CLI (cldkctl) integration."""

import asyncio
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import anyio
import click
import mcp.types as types
from mcp.server.lowlevel import Server
from rich.console import Console
from rich.panel import Panel

console = Console()


class CldkctlExecutor:
    """Executor for cldkctl commands."""
    
    def __init__(self, cldkctl_path: Optional[str] = None):
        # Default to the authenticated cldkctl binary
        if cldkctl_path is None:
            # Try to find cldkctl in common locations
            possible_paths = [
                "cldkctl",
                "cldkctl.exe",
                "../ai-cldkctl/cldkctl",
                "../ai-cldkctl/cldkctl.exe",
                "C:/__LINTAS/MCP/MCP-CLDKCTL/ai-cldkctl/cldkctl",
                "C:/__LINTAS/MCP/MCP-CLDKCTL/ai-cldkctl/cldkctl.exe"
            ]
            
            for path in possible_paths:
                if Path(path).exists():
                    cldkctl_path = path
                    break
            else:
                cldkctl_path = "cldkctl"  # fallback
        
        self.cldkctl_path = cldkctl_path
    
    async def execute_command(self, args: List[str]) -> tuple[int, str, str]:
        """Execute a cldkctl command and return (return_code, stdout, stderr)."""
        try:
            process = await asyncio.create_subprocess_exec(
                self.cldkctl_path,
                *args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            # Decode bytes to string for Python <3.11
            stdout = stdout.decode() if stdout else ""
            stderr = stderr.decode() if stderr else ""
            
            return process.returncode, stdout, stderr
        except Exception as e:
            return 1, "", str(e)
    
    def format_output(self, stdout: str, stderr: str, return_code: int) -> str:
        """Format command output for display."""
        if return_code != 0:
            return f"Error (exit code {return_code}):\n{stderr or stdout}"
        return stdout.strip() if stdout else "Command executed successfully."


# Global executor instance
executor = CldkctlExecutor()


async def run_cldkctl_command(command: str, subcommand: str = "", args: List[str] = None) -> str:
    """Run a cldkctl command and return formatted output."""
    cmd_args = [command]
    if subcommand:
        cmd_args.append(subcommand)
    if args:
        cmd_args.extend(args)
    
    return_code, stdout, stderr = await executor.execute_command(cmd_args)
    return executor.format_output(stdout, stderr, return_code)


@click.command()
@click.option("--port", default=8000, help="Port to listen on for SSE")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport type",
)
@click.option(
    "--cldkctl-path",
    help="Path to cldkctl binary",
    default=None
)
def main(port: int, transport: str, cldkctl_path: str) -> int:
    """MCP server for Cloudeka CLI integration."""
    global executor
    executor = CldkctlExecutor(cldkctl_path)
    
    app = Server("mcp-cldkctl")

    @app.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[types.ContentBlock]:
        """Handle tool calls."""
        try:
            if name == "auth":
                return await handle_auth(arguments)
            elif name == "balance":
                return await handle_balance(arguments)
            elif name == "billing":
                return await handle_billing(arguments)
            elif name == "kubernetes":
                return await handle_kubernetes(arguments)
            elif name == "organization":
                return await handle_organization(arguments)
            elif name == "profile":
                return await handle_profile(arguments)
            elif name == "project":
                return await handle_project(arguments)
            elif name == "registry":
                return await handle_registry(arguments)
            elif name == "vm":
                return await handle_vm(arguments)
            elif name == "voucher":
                return await handle_voucher(arguments)
            elif name == "notebook":
                return await handle_notebook(arguments)
            elif name == "logs":
                return await handle_logs(arguments)
            elif name == "token":
                return await handle_token(arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        """List available tools."""
        return [
            # Authentication
            types.Tool(
                name="auth",
                title="Authentication",
                description="Authenticate with Cloudeka service using token",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "token": {
                            "type": "string",
                            "description": "Authentication token"
                        }
                    }
                }
            ),
            
            # Balance
            types.Tool(
                name="balance",
                title="Balance",
                description="View balance for each project",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project": {
                            "type": "string",
                            "description": "Project ID (optional)"
                        }
                    }
                }
            ),
            
            # Billing
            types.Tool(
                name="billing",
                title="Billing",
                description="View project billing details",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project": {
                            "type": "string",
                            "description": "Project ID"
                        },
                        "month": {
                            "type": "string",
                            "description": "Billing month (YYYY-MM format)"
                        }
                    }
                }
            ),
            
            # Kubernetes
            types.Tool(
                name="kubernetes",
                title="Kubernetes Management",
                description="Manage Kubernetes resources",
                inputSchema={
                    "type": "object",
                    "required": ["resource", "action"],
                    "properties": {
                        "resource": {
                            "type": "string",
                            "enum": ["pods", "deployments", "services", "configmaps", "secrets", "namespaces", "ingresses", "daemonsets", "statefulsets", "persistentvolumes", "persistentvolumeclaims"],
                            "description": "Kubernetes resource type"
                        },
                        "action": {
                            "type": "string",
                            "enum": ["list", "get", "describe", "logs"],
                            "description": "Action to perform"
                        },
                        "name": {
                            "type": "string",
                            "description": "Resource name (for get/describe actions)"
                        },
                        "namespace": {
                            "type": "string",
                            "description": "Namespace (default: default)"
                        }
                    }
                }
            ),
            
            # Organization
            types.Tool(
                name="organization",
                title="Organization Management",
                description="Manage organization details, members, and roles",
                inputSchema={
                    "type": "object",
                    "required": ["action"],
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["list", "get", "members", "roles"],
                            "description": "Action to perform"
                        },
                        "org_id": {
                            "type": "string",
                            "description": "Organization ID"
                        }
                    }
                }
            ),
            
            # Profile
            types.Tool(
                name="profile",
                title="Profile Management",
                description="View and manage your profile information",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["get", "update"],
                            "description": "Action to perform"
                        }
                    }
                }
            ),
            
            # Project
            types.Tool(
                name="project",
                title="Project Management",
                description="View and manage your projects",
                inputSchema={
                    "type": "object",
                    "required": ["action"],
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["list", "get", "create", "delete"],
                            "description": "Action to perform"
                        },
                        "project_id": {
                            "type": "string",
                            "description": "Project ID"
                        },
                        "name": {
                            "type": "string",
                            "description": "Project name (for create action)"
                        }
                    }
                }
            ),
            
            # Registry
            types.Tool(
                name="registry",
                title="Container Registry",
                description="Manage your container registry",
                inputSchema={
                    "type": "object",
                    "required": ["action"],
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["list", "get", "create", "delete", "push", "pull"],
                            "description": "Action to perform"
                        },
                        "registry": {
                            "type": "string",
                            "description": "Registry name"
                        },
                        "image": {
                            "type": "string",
                            "description": "Image name"
                        },
                        "tag": {
                            "type": "string",
                            "description": "Image tag"
                        }
                    }
                }
            ),
            
            # VMs
            types.Tool(
                name="vm",
                title="Virtual Machine Management",
                description="Manage virtual machines (VMs)",
                inputSchema={
                    "type": "object",
                    "required": ["action"],
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["list", "get", "create", "delete", "start", "stop", "restart"],
                            "description": "Action to perform"
                        },
                        "vm_id": {
                            "type": "string",
                            "description": "VM ID"
                        },
                        "name": {
                            "type": "string",
                            "description": "VM name (for create action)"
                        }
                    }
                }
            ),
            
            # Voucher
            types.Tool(
                name="voucher",
                title="Voucher Management",
                description="Manage project vouchers and credit balances",
                inputSchema={
                    "type": "object",
                    "required": ["action"],
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["list", "get", "create", "redeem"],
                            "description": "Action to perform"
                        },
                        "voucher_id": {
                            "type": "string",
                            "description": "Voucher ID"
                        },
                        "code": {
                            "type": "string",
                            "description": "Voucher code (for redeem action)"
                        }
                    }
                }
            ),
            
            # Notebook
            types.Tool(
                name="notebook",
                title="Notebook Management",
                description="Manage notebooks",
                inputSchema={
                    "type": "object",
                    "required": ["action"],
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["list", "get", "create", "delete", "start", "stop"],
                            "description": "Action to perform"
                        },
                        "notebook_id": {
                            "type": "string",
                            "description": "Notebook ID"
                        },
                        "name": {
                            "type": "string",
                            "description": "Notebook name (for create action)"
                        }
                    }
                }
            ),
            
            # Logs
            types.Tool(
                name="logs",
                title="Audit Logs",
                description="View and manage activity logs in the organization's cloud",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["list", "get"],
                            "description": "Action to perform"
                        },
                        "log_id": {
                            "type": "string",
                            "description": "Log ID (for get action)"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Number of logs to retrieve"
                        }
                    }
                }
            ),
            
            # Token
            types.Tool(
                name="token",
                title="Token Management",
                description="View and manage your Cloudeka authentication tokens",
                inputSchema={
                    "type": "object",
                    "required": ["action"],
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["list", "get", "create", "delete"],
                            "description": "Action to perform"
                        },
                        "token_id": {
                            "type": "string",
                            "description": "Token ID"
                        }
                    }
                }
            ),
        ]

    # Tool handlers
    async def handle_auth(arguments: dict) -> list[types.ContentBlock]:
        """Handle authentication."""
        token = arguments.get("token", "")
        if not token:
            return [types.TextContent(type="text", text="Error: Token is required for authentication")]
        
        result = await run_cldkctl_command("auth", args=[token])
        return [types.TextContent(type="text", text=result)]

    async def handle_balance(arguments: dict) -> list[types.ContentBlock]:
        """Handle balance command."""
        project = arguments.get("project", "")
        args = []
        if project:
            args.extend(["--project", project])
        
        result = await run_cldkctl_command("balance", args=args)
        return [types.TextContent(type="text", text=result)]

    async def handle_billing(arguments: dict) -> list[types.ContentBlock]:
        """Handle billing command."""
        project = arguments.get("project", "")
        month = arguments.get("month", "")
        
        if not project:
            return [types.TextContent(type="text", text="Error: Project ID is required for billing")]
        
        args = ["--project", project]
        if month:
            args.extend(["--month", month])
        
        result = await run_cldkctl_command("billing", args=args)
        return [types.TextContent(type="text", text=result)]

    async def handle_kubernetes(arguments: dict) -> list[types.ContentBlock]:
        """Handle kubernetes commands."""
        resource = arguments.get("resource", "")
        action = arguments.get("action", "")
        name = arguments.get("name", "")
        namespace = arguments.get("namespace", "")
        
        if not resource or not action:
            return [types.TextContent(type="text", text="Error: Resource and action are required")]
        
        args = [resource, action]
        if name:
            args.append(name)
        if namespace:
            args.extend(["--namespace", namespace])
        
        result = await run_cldkctl_command("kubernetes", args=args)
        return [types.TextContent(type="text", text=result)]

    async def handle_organization(arguments: dict) -> list[types.ContentBlock]:
        """Handle organization commands."""
        action = arguments.get("action", "")
        org_id = arguments.get("org_id", "")
        
        if not action:
            return [types.TextContent(type="text", text="Error: Action is required")]
        
        args = [action]
        if org_id:
            args.extend(["--org", org_id])
        
        result = await run_cldkctl_command("organization", args=args)
        return [types.TextContent(type="text", text=result)]

    async def handle_profile(arguments: dict) -> list[types.ContentBlock]:
        """Handle profile commands."""
        action = arguments.get("action", "get")
        args = [action] if action != "get" else []
        
        result = await run_cldkctl_command("profile", args=args)
        return [types.TextContent(type="text", text=result)]

    async def handle_project(arguments: dict) -> list[types.ContentBlock]:
        """Handle project commands."""
        action = arguments.get("action", "")
        project_id = arguments.get("project_id", "")
        name = arguments.get("name", "")
        
        if not action:
            return [types.TextContent(type="text", text="Error: Action is required")]
        
        args = [action]
        if project_id:
            args.extend(["--project", project_id])
        if name:
            args.extend(["--name", name])
        
        result = await run_cldkctl_command("project", args=args)
        return [types.TextContent(type="text", text=result)]

    async def handle_registry(arguments: dict) -> list[types.ContentBlock]:
        """Handle registry commands."""
        action = arguments.get("action", "")
        registry = arguments.get("registry", "")
        image = arguments.get("image", "")
        tag = arguments.get("tag", "")
        
        if not action:
            return [types.TextContent(type="text", text="Error: Action is required")]
        
        args = [action]
        if registry:
            args.extend(["--registry", registry])
        if image:
            args.extend(["--image", image])
        if tag:
            args.extend(["--tag", tag])
        
        result = await run_cldkctl_command("registry", args=args)
        return [types.TextContent(type="text", text=result)]

    async def handle_vm(arguments: dict) -> list[types.ContentBlock]:
        """Handle VM commands."""
        action = arguments.get("action", "")
        vm_id = arguments.get("vm_id", "")
        name = arguments.get("name", "")
        
        if not action:
            return [types.TextContent(type="text", text="Error: Action is required")]
        
        args = [action]
        if vm_id:
            args.extend(["--vm", vm_id])
        if name:
            args.extend(["--name", name])
        
        result = await run_cldkctl_command("vm", args=args)
        return [types.TextContent(type="text", text=result)]

    async def handle_voucher(arguments: dict) -> list[types.ContentBlock]:
        """Handle voucher commands."""
        action = arguments.get("action", "")
        voucher_id = arguments.get("voucher_id", "")
        code = arguments.get("code", "")
        
        if not action:
            return [types.TextContent(type="text", text="Error: Action is required")]
        
        args = [action]
        if voucher_id:
            args.extend(["--voucher", voucher_id])
        if code:
            args.extend(["--code", code])
        
        result = await run_cldkctl_command("voucher", args=args)
        return [types.TextContent(type="text", text=result)]

    async def handle_notebook(arguments: dict) -> list[types.ContentBlock]:
        """Handle notebook commands."""
        action = arguments.get("action", "")
        notebook_id = arguments.get("notebook_id", "")
        name = arguments.get("name", "")
        
        if not action:
            return [types.TextContent(type="text", text="Error: Action is required")]
        
        args = [action]
        if notebook_id:
            args.extend(["--notebook", notebook_id])
        if name:
            args.extend(["--name", name])
        
        result = await run_cldkctl_command("notebook", args=args)
        return [types.TextContent(type="text", text=result)]

    async def handle_logs(arguments: dict) -> list[types.ContentBlock]:
        """Handle logs commands."""
        action = arguments.get("action", "list")
        log_id = arguments.get("log_id", "")
        limit = arguments.get("limit", "")
        
        args = [action]
        if log_id:
            args.extend(["--log", log_id])
        if limit:
            args.extend(["--limit", str(limit)])
        
        result = await run_cldkctl_command("logs", args=args)
        return [types.TextContent(type="text", text=result)]

    async def handle_token(arguments: dict) -> list[types.ContentBlock]:
        """Handle token commands."""
        action = arguments.get("action", "")
        token_id = arguments.get("token_id", "")
        
        if not action:
            return [types.TextContent(type="text", text="Error: Action is required")]
        
        args = [action]
        if token_id:
            args.extend(["--token", token_id])
        
        result = await run_cldkctl_command("token", args=args)
        return [types.TextContent(type="text", text=result)]

    if transport == "sse":
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.responses import Response
        from starlette.routing import Mount, Route

        sse = SseServerTransport("/messages/")

        async def handle_sse(request):
            async with sse.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )
            return Response()

        starlette_app = Starlette(
            debug=True,
            routes=[
                Route("/sse", endpoint=handle_sse, methods=["GET"]),
                Mount("/messages/", app=sse.handle_post_message),
            ],
        )

        import uvicorn
        uvicorn.run(starlette_app, host="127.0.0.1", port=port)
    else:
        from mcp.server.stdio import stdio_server

        async def arun():
            async with stdio_server() as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )

        anyio.run(arun)

    return 0


if __name__ == "__main__":
    sys.exit(main()) 