import argparse
from .core import download_model

def download_model_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_id", help="HuggingFace repo id")
    parser.add_argument("local_dir", help="Directory to store downloaded files")
    args = parser.parse_args()

    download_model(args.repo_id, args.local_dir)

