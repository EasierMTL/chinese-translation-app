from enum import Enum
import os
import gdown

model_params = {
    "quantize_dynamic": {
        "file_id": "1Bhd2B3UoUuIr9hQROLsqhpzUp3-1vL12",
        "save_path": "dynamic_quantized.pt"
    }
}


def download_model(save_path: str, file_id: str):
    print(f"Downloading {file_id} at {save_path}")
    gdown.download(id=file_id, output=save_path, quiet=False)
    print("Downloaded!")


if __name__ == "__main__":
    download_model(os.path.join("saved_models", "quantized.pt"),
                   model_params["quantize_dynamic"]["file_id"])
