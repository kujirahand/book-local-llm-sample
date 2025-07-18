"""MCPサーバーに接続してツールを呼び出す"""
import asyncio
from fastmcp import Client

async def main():
    # MCPクライアントの初期化 --- (*1)
    client = Client("http://127.0.0.1:8000/mcp")
    async with client:
        # MCPサーバーに接続確認を行う --- (*2)
        await client.ping()
        # 利用可能なツールのリストを取得 --- (*3)
        tools = await client.list_tools()
        print("利用可能なツール:", [tool.name for tool in tools])
        # 足し算ツールを呼び出す --- (*4)
        result = await client.call_tool("add", {"a": 5, "b": 7})
        # 結果を表示 --- (*5)
        print("結果:", result.data)

asyncio.run(main())
