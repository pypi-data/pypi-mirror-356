from .dataeyes import mcp

def main():
    """MCP Dataeyes Server - HTTP call Dataeyes API for MCP"""
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()