#from .dataeyes import mcp
import dataeyes_mcp_server 
#def main():
#    """MCP Dataeyes Server - HTTP call Dataeyes API for MCP"""
#    dataeyes(transport="stdio")

if __name__ == "__main__":
    dataeyes_mcp_server.dataeyes()