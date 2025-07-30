import anyio
from mcp_cldkctl.server import main

def main_entry():
    anyio.run(main)

if __name__ == "__main__":
    main_entry() 