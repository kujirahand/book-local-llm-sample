#!/bin/sh
prompt='### Instruction:
次の手順で段階的に考えて、最終的に日本語で答えを提出してください。
1. 可愛いの定義を考えて述べてください。
2. 次に可愛い猫の名前を3つ考えて、その理由を答えてください。
3. 上記の名前を一つずつ精査して、最終的に1つだけを選んでください。
4. 回答を下記のJSON形式で出力してください。
### Output:
```json
{
    "answer": "<猫の名前>",
    "selection": ["名前1", "名前2", "名前3"]
}
```'
ollama run llama3.2:3b --verbose "$prompt"
ollama run qwen3:8b --verbose "$prompt"

