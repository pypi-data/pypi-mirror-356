from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="Demo")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def sub(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b