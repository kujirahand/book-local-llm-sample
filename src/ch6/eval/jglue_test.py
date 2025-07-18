import jcommonsenseqa
import jsquad
import jsts
import jnli

LLM_MODELS = ["gemma3:4b", "gemma3n:e4b", "llama3.1:8b", "qwen3:8b", "deepseek-r1:8b"]
# LLM_MODELS = ["gemma3:4b"]

def main():
    """メイン関数"""
    result = {
        "jcommonsenseqa": {},
        "jsquad": {},
        "jnli": {},
        "jsts": {},
    }
    for model in LLM_MODELS:
        print(f"モデル: {model}")
        # JCommonsenseQAのテスト
        acc = jcommonsenseqa.do_test(model)
        result["jcommonsenseqa"][model] = acc
        # JSQuADのテスト
        acc = jsquad.do_test(model)
        result["jsquad"][model] = acc
        # JNLIのテスト
        acc = jnli.do_test(model)
        result["jnli"][model] = acc
        # JSTSのテスト
        acc = jsts.do_test(model)
        result["jsts"][model] = acc
    # 結果をCSVで出力
    print("### テスト結果:")
    print("モデル, JCommonsenseQA, JSQuAD, JNLI, JSTS")
    for model in LLM_MODELS:
        jcommonsenseqa_acc = result["jcommonsenseqa"][model] * 100
        jsquad_acc = result["jsquad"][model] * 100
        jsts_acc = result["jsts"][model]
        jnli_acc = result["jnli"][model] * 100
        print(f"{model}, {jcommonsenseqa_acc:.0f}%, {jsquad_acc:.0f}%, {jnli_acc:.0f}%, {jsts_acc:.2f}")

if __name__ == "__main__":
    main()