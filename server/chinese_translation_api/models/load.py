import os
import gdown

model_params = {
    # https://drive.google.com/file/d/1-fqBWI7rpZK5DdZc2pRYTZfWuZEsBPhR/view?usp=share_link
    "quantized_dynamic": {
        "file_id": "1-fqBWI7rpZK5DdZc2pRYTZfWuZEsBPhR",
        "save_path": "dynamic_quantized.pt",
    }
}


def download_model(save_path: str, file_id: str):
    print(f"Downloading {file_id} at {save_path}")
    gdown.download(id=file_id, output=save_path, quiet=False)
    print("Downloaded!")


if __name__ == "__main__":
    download_model(
        os.path.join("saved_models", "quantized.pt"),
        model_params["quantized_dynamic"]["file_id"],
    )
