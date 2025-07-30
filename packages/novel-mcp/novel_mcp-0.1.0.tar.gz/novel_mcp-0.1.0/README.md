# Novel MCP

[![PyPI version](https://badge.fury.io/py/novel-mcp.svg)](https://badge.fury.io/py/novel-mcp)
[![Python Support](https://img.shields.io/pypi/pyversions/novel-mcp.svg)](https://pypi.org/project/novel-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Model Context Protocol (MCP) server for novel processing with mathematical operations.

## 项目概述

Novel MCP 是一个基于 FastMCP 的服务器，提供小说处理和数学运算等功能。它实现了 Model Context Protocol，可以与支持 MCP 的客户端进行交互。

## 功能特性

- ✅ 基于 FastMCP 框架
- ✅ 提供数学运算工具（加法、乘法）
- ✅ 支持 stdio 传输协议
- ✅ 可扩展的工具系统
- ✅ 完整的类型注解

## 安装

### 从 PyPI 安装

```bash
pip install novel-mcp
```

### 从源码安装

```bash
git clone https://github.com/yourusername/novel-mcp.git
cd novel-mcp
pip install -e .
```

## 使用方法

### 作为命令行工具运行

安装后，你可以直接运行：

```bash
novel-mcp
```

### 作为 Python 模块使用

```python
from novel_mcp import mcp

# 运行服务器
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### 在 MCP 客户端中配置

在支持 MCP 的客户端（如 Claude Desktop）中配置：

```json
{
  "mcpServers": {
    "novel_server": {
      "command": "novel-mcp",
      "args": [],
      "env": {}
    }
  }
}
```

或者如果你是从源码运行：

```json
{
  "mcpServers": {
    "novel_server": {
      "command": "python",
      "args": [
        "/path/to/novel_mcp/main.py"
      ],
      "env": {}
    }
  }
}
```

## 可用工具

### add(a: int, b: int) -> int
加法运算工具，计算两个整数的和。

**参数：**
- `a`: 第一个数字
- `b`: 第二个数字

**返回：** 两数之和

### multiply(a: int, b: int) -> int
乘法运算工具，计算两个整数的乘积。

**参数：**
- `a`: 第一个数字
- `b`: 第二个数字

**返回：** 两数之积

## 开发

### 环境设置

```bash
# 克隆项目
git clone https://github.com/yourusername/novel-mcp.git
cd novel-mcp

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装开发依赖
pip install -e ".[dev]"
```

### 运行测试

```bash
pytest
```

### 代码格式化

```bash
black novel_mcp/
isort novel_mcp/
```

## 项目结构

```
novel_mcp/
├── __init__.py          # 包初始化文件
├── main.py             # MCP服务器主文件
├── mcp_client.py       # MCP客户端测试文件
├── mcp_sse.py          # SSE协议支持
├── pyproject.toml      # 项目配置文件
├── README.md           # 项目说明
└── LICENSE             # 许可证文件
```

## 技术栈

- **FastMCP**: Model Context Protocol 框架
- **Python 3.8+**: 编程语言
- **Type Hints**: 完整的类型注解支持

## 贡献

欢迎贡献代码！请遵循以下步骤：

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 更新日志

### v0.1.0
- 初始版本发布
- 支持基本的数学运算（加法、乘法）
- 实现 MCP 协议支持

## 支持

如果你遇到问题或有建议，请：

1. 查看 [Issues](https://github.com/yourusername/novel-mcp/issues)
2. 创建新的 Issue
3. 或者直接提交 Pull Request

---

**注意：** 请将 README 中的 `yourusername` 替换为你的实际 GitHub 用户名，并更新作者信息。