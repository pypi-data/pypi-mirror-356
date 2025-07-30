from mcp import Client
import asyncio

# MCP服务器配置
config = {
    "mcpServers": {
        "novel_server": {"command": "python", "args": ["./main.py"]}
    }
}

# 创建客户端连接到服务器
client = Client(config)

def extract_result(result):
    """从MCP响应中提取实际结果"""
    if isinstance(result, list) and len(result) > 0:
        # 如果结果是TextContent列表，提取文本内容
        if hasattr(result[0], 'text'):
            return result[0].text
        return result[0]
    return result

async def list_available_tools():
    """获取可用的工具列表"""
    try:
        tools = await client.list_tools()
        print("可用的工具:")
        for tool in tools:
            # 修复Tool对象访问方式
            tool_name = getattr(tool, 'name', 'unknown')
            tool_desc = getattr(tool, 'description', '无描述')
            print(f"  - {tool_name}: {tool_desc}")
        return tools
    except Exception as e:
        print(f"获取工具列表失败: {e}")
        return []

async def test_math_operations():
    """测试数学运算工具"""
    try:
        print("\n=== 测试数学运算工具 ===")
        
        # 测试加法
        result_add = await client.call_tool("add", {"a": 10, "b": 5})
        result_add = extract_result(result_add)
        print(f"10 + 5 = {result_add}")
        
        # 测试乘法
        result_multiply = await client.call_tool("multiply", {"a": 6, "b": 7})
        result_multiply = extract_result(result_multiply)
        print(f"6 × 7 = {result_multiply}")
        
        # 更多测试用例
        test_cases = [
            ("add", {"a": 100, "b": 200}, "100 + 200"),
            ("multiply", {"a": 12, "b": 8}, "12 × 8"),
            ("add", {"a": -5, "b": 3}, "-5 + 3"),
            ("multiply", {"a": 0, "b": 10}, "0 × 10")
        ]
        
        print("\n=== 批量测试 ===")
        for tool_name, params, display in test_cases:
            result = await client.call_tool(tool_name, params)
            result = extract_result(result)
            print(f"{display} = {result}")
                
    except Exception as e:
        print(f"测试数学运算时发生错误: {e}")

async def interactive_calculator():
    """交互式计算器"""
    print("\n=== 交互式计算器（输入 'quit' 退出）===")
    
    while True:
        try:
            operation = input("请选择操作 (add/multiply): ").strip().lower()
            if operation == 'quit':
                break
                
            if operation not in ['add', 'multiply']:
                print("请输入 'add' 或 'multiply'")
                continue
                
            a = int(input("输入第一个数字: "))
            b = int(input("输入第二个数字: "))
            
            result = await client.call_tool(operation, {"a": a, "b": b})
            result = extract_result(result)
            
            operator = "+" if operation == "add" else "×"
            print(f"结果: {a} {operator} {b} = {result}\n")
            
        except ValueError:
            print("请输入有效的整数")
        except KeyboardInterrupt:
            print("\n退出交互式计算器")
            break
        except Exception as e:
            print(f"计算出错: {e}")

async def main():
    """主函数"""
    async with client:
        print("=== MCP客户端启动 ===")
        
        # 获取可用工具列表
        await list_available_tools()
        
        # 测试数学运算功能
        await test_math_operations()
        
        # 交互式计算器（可选）
        user_input = input("\n是否启动交互式计算器？(y/n): ").strip().lower()
        if user_input in ['y', 'yes']:
            await interactive_calculator()
        
        print("\n=== MCP客户端测试完成 ===")

if __name__ == "__main__":
    asyncio.run(main())