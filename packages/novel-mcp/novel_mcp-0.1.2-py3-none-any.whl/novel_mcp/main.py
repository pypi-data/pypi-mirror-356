from mcp.server.fastmcp import FastMCP

# 创建 MCP 服务器实例
mcp = FastMCP("novel_server")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of a and b
    """
    return a + b

if __name__ == "__main__":
    mcp.run(transport="stdio")