#!/usr/bin/env python3
"""Simplified server for testing uvx integration without MCP dependencies."""

import asyncio
import logging
import subprocess
import sys
import traceback
from pathlib import Path
from typing import List, Optional

import click

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


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
                    logger.info(f"Found cldkctl at: {path}")
                    break
            else:
                cldkctl_path = "cldkctl"  # fallback
                logger.warning("cldkctl not found in common locations, using fallback")
        
        self.cldkctl_path = cldkctl_path
        logger.info(f"Initialized CldkctlExecutor with path: {cldkctl_path}")
    
    async def execute_command(self, args: List[str]) -> tuple[int, str, str]:
        """Execute a cldkctl command and return (return_code, stdout, stderr)."""
        try:
            logger.info(f"Executing: {self.cldkctl_path} {' '.join(args)}")
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
            
            logger.info(f"Command completed with return code: {process.returncode}")
            if stderr:
                logger.warning(f"Command stderr: {stderr}")
            
            return process.returncode, stdout, stderr
        except Exception as e:
            logger.error(f"Exception executing command: {e}")
            logger.error(traceback.format_exc())
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
@click.option("--test", is_flag=True, help="Run a test command")
@click.option("--cldkctl-path", help="Path to cldkctl binary", default=None)
def main(test: bool, cldkctl_path: str) -> int:
    """Simplified MCP server for Cloudeka CLI integration."""
    try:
        logger.info("Starting simplified MCP cldkctl server...")
        
        global executor
        executor = CldkctlExecutor(cldkctl_path)
        
        if test:
            logger.info("Running test command...")
            # Run a simple test
            result = asyncio.run(run_cldkctl_command("--version"))
            print(f"Test result: {result}")
            return 0
        
        logger.info("Server initialized successfully")
        print("✅ MCP cldkctl server is ready!")
        print("🔧 Available commands:")
        print("  - auth: Authentication")
        print("  - balance: View balances")
        print("  - billing: View billing")
        print("  - kubernetes: Manage K8s resources")
        print("  - organization: Manage organizations")
        print("  - profile: User profile")
        print("  - project: Project management")
        print("  - registry: Container registry")
        print("  - vm: Virtual machines")
        print("  - voucher: Voucher management")
        print("  - notebook: Notebook management")
        print("  - logs: Audit logs")
        print("  - token: Token management")
        
        print("\n📋 Usage with uvx:")
        print("uvx mcp-cldkctl --test")
        
        return 0
        
    except Exception as e:
        logger.error(f"Fatal error in main: {e}")
        logger.error(traceback.format_exc())
        print(f"Fatal error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main()) 