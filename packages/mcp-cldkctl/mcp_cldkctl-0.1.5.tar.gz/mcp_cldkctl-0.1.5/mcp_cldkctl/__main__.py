# import anyio
# from mcp_cldkctl.server import main

# def main_entry():
#     anyio.run(main)

# if __name__ == "__main__":
#     main_entry() 


# import anyio
# main.py
# from mcp.server.fastmcp import FastMCP

# mcp = FastMCP("My App")

# if __name__ == "__main__":
#     mcp.run()


# main.py

import logging
logger = logging.getLogger(__name__)
logger.info("tes0")

from .server import mcp
logger.info("tes2")

def main():
    """Entry point for the mcp_cldkctl script."""
    mcp.run()

if __name__ == "__main__":
    main()