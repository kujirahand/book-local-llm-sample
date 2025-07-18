# mcp_add_client.py
import asyncio
from fastmcp import Client
import ollama
import json

# OllamaのChatモデルの設定
LLM_MODEL = "qwen3:8b"
# LLMのプロンプトテンプレート --- (*1)
LLM_PROMPT = """\
あなたは優秀なAIアシスタントです。
ユーザーの質問に対して、適切な回答を提供してください。
あなたは、次のツールを利用できます。可能なら以下のツールを利用してください。
{tools}
なお、ツールを呼び出す際は、次のフォーマットの出力のみを出力してください。
```
{{"tool": "ツール名", "args": {{ "引数名": "値", "引数名": "値" }} }}
```
"""

async def main():
    # MCPクライアントの初期化 --- (*2)
    client = Client("http://127.0.0.1:8001/mcp")
    async with client:
        await client.ping()
        # 利用可能なツールのリストを取得 --- (*3)
        desc = ""
        tools = await client.list_tools()
        for tool in tools:
            desc += f"- ツール名: {tool.name}\n"
            desc += f"  - 説明: {tool.description}\n"
            desc += f"  - 引数: {json.dumps(tool.inputSchema['properties'])}\n"
            if tool.outputSchema:
                desc += f"  - 出力: {json.dumps(tool.outputSchema['properties'])}\n"
        print("利用可能なツールの説明:")
        print(desc)
        # OllamaのChatモデルを初期化 --- (*4)
        sys_prompt = LLM_PROMPT.format(tools=", ".join(tool.name for tool in tools))
        messages = [{"role": "system", "content": sys_prompt}]
        # チャットのメインループ --- (*5)
        while True:
            print("-" * 60)
            print("終了するときは'q'を入力してください。")
            user_input = input(">>> ")
            if user_input.lower() == 'q':
                break
            if user_input.strip() == "":
                continue
            # ユーザーの入力をメッセージに追加 --- (*6)
            messages.append({"role": "user", "content": user_input})
            # OllamaのChatモデルを使用して応答を生成 --- (*7)
            response = ollama.chat(LLM_MODEL, messages)
            res = response["message"]["content"]
            if "</think>" in res: # --- (*8)
                res = res.split("</think>")[-1].strip()
            print("<<< ", res)
            # 応答をメッセージに追加 --- (*9)
            messages.append({"role": "assistant", "content": res})
            # ツール呼び出しの解析 --- (*10)
            if res.startswith("```") and res.endswith("```"):
                res = res[3:-3].strip()
            if res.startswith("{") and res.endswith("}"):
                try:
                    r = json.loads(res)
                except json.JSONDecodeError:
                    print("<<< ツール呼び出しの解析に失敗:", res)
                    continue
                tool_name = r.get("tool", "")
                args = r.get("args", {})
                if tool_name and args:
                    # MCPツールの呼び出し --- (*11)
                    print(f"<<< MCPツールの呼び出し: {tool_name}({args})")
                    result = await client.call_tool(tool_name, args)
                    if result.is_error:
                        print("ツールの呼び出しエラー")
                        continue
                    print("<<< ツールの結果:", result.data)
if __name__ == "__main__":
    asyncio.run(main())
