from .server import main
import sys
import traceback

def main_wrapper():
    """Entry point for the mcp_cldkctl script."""
    try:
        import asyncio
        asyncio.run(main())
    except Exception as e:
        print("Fatal error in mcp_cldkctl:", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main_wrapper()