"""Entry point for mcp-cldkctl when run with uvx."""

import sys
from .server import main

if __name__ == "__main__":
    sys.exit(main()) 