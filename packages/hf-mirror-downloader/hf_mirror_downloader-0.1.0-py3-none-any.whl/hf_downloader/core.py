import subprocess
import os

def download_model(repo_id: str, local_dir: str):
    env = os.environ.copy()
    env["HF_ENDPOINT"] = "https://hf-mirror.com"

    cmd = [
        "huggingface-cli",
        "download",
        "--resume-download",
        repo_id,
        "--local-dir", local_dir,
        "--local-dir-use-symlinks", "False"
    ]

    result = subprocess.run(cmd, env=env)
    if result.returncode != 0:
        raise RuntimeError("Download failed.")