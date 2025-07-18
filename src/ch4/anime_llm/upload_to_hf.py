from huggingface_hub import HfApi

repo_id = "kujirahand/llama3_anime_llm"
folder_path = "./model_merged"

api = HfApi()
api.upload_folder(
    folder_path=folder_path,
    repo_id=repo_id,
    repo_type="model"
)
