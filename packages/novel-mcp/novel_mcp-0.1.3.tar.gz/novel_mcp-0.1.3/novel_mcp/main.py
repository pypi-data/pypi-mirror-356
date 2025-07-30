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


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Product of a and b
    """
    return a * b


def main():
    """主入口函数，用于命令行启动"""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()