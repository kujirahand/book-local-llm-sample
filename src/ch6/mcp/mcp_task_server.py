"""計算などのタスクを行うMCPサーバー"""
import warnings
from fastmcp import FastMCP
warnings.filterwarnings("ignore", category=DeprecationWarning)

# FastMCPサーバーの初期化 --- (*1)
mcp = FastMCP("TaskServer")

# 足し算ツールの定義 --- (*2)
@mcp.tool()
def add(a: int, b: int) -> int:
    """a と b を足して返す"""
    return a + b

# 掛け算ツールの定義 --- (*3)
@mcp.tool()
def mul(a: int, b: int) -> int:
    """a と b を掛け算して返す"""
    return a * b

# 挨拶ツールの定義 --- (*4)
@mcp.tool()
def hello(name: str) -> str:
    """nameに挨拶して返す"""
    return f"{name}さん、こんにちは！"

if __name__ == "__main__":
    # HTTPモードで起動 --- (*5)
    mcp.run(transport="http", host="127.0.0.1", port=8001)
