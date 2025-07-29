from huggingface_hub import snapshot_download
import os

model_name = 'deepseek-ai/DeepSeek-R1-0528-Qwen3-8B'
# 定义Triton模型仓库中该模型的版本路径
local_model_path = os.path.join("models", "deepseek_r1", "1")

print(f"开始下载模型 '{model_name}' 到 '{local_model_path}'...")

# 使用 snapshot_download 下载整个模型仓库
# 它会下载所有文件，包括.safetensors权重文件
snapshot_download(
    repo_id=model_name,
    local_dir=local_model_path,
    local_dir_use_symlinks=False,  
)

print("模型所有文件下载完成!")