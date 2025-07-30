from mcp.server.fastmcp import FastMCP
from datetime import datetime

# Create an MCP server
mcp = FastMCP("Demo")

# 基本数学工具
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract b from a"""
    return a - b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide a by b"""
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return a / b

# 文本处理工具
@mcp.tool()
def echo(message: str) -> str:
    """Echo the input message"""
    return message

@mcp.tool()
def uppercase(text: str) -> str:
    """Convert text to uppercase"""
    return text.upper()

# 动态资源：个性化问候
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}! Welcome to FastMCP."

# 动态资源：服务器当前时间
@mcp.resource("time://now")
def get_current_time() -> str:
    """Get server current date and time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 动态资源：用户配置示例
@mcp.resource("config://{section}/{key}")
def get_config(section: str, key: str) -> str:
    """Retrieve configuration value (示例)"""
    # 在实际应用中，这里可以接入配置文件或数据库
    sample_config = {
        "database": {"host": "localhost", "port": 5432},
        "app": {"debug": True, "version": "1.0.0"}
    }
    return str(sample_config.get(section, {}).get(key, "<undefined>"))

def main() -> None:
    mcp.run(transport='stdio')
