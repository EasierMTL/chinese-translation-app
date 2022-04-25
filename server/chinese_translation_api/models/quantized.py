import torch
import torch.quantization
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


def create_quantized_model():
    """Creates the chinese to english quantized model.
    """

    model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-zh-en")
    quantized_model = torch.quantization.quantize_dynamic(model,
                                                          {torch.nn.Linear},
                                                          dtype=torch.qint8)
    return quantized_model


def create_save_quantized_model(save_path: str):
    """Create and save quantized CH to English model
    """
    quantized_model = create_quantized_model()
    quantized_model.eval()
    torch.save(quantized_model, save_path)
    return quantized_model


# wget https://raw.githubusercontent.com/Helsinki-NLP/Tatoeba-Challenge/master/data/test/eng-zho/test.txt

# def traced_quantized_model(save_path: str):
#     base_shape = [1, None]
#     input

if __name__ == "__main__":
    # poetry run python api/models/quantized.py
    print("Creating quantized model...")
    quantized_model_path = "./quantized_translator.pt"
    create_save_quantized_model(quantized_model_path)
    print("Loading and predicting an example batch...")
    tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-zh-en")
    model = torch.load(quantized_model_path)

    def predict_quantized(message):
        """Runs the prediction pipeline.
        """
        inputs = tokenizer(message, return_tensors="pt")
        print(inputs)
        print(inputs["input_ids"].shape)
        translated = model.generate(**inputs)
        translated_text = tokenizer.batch_decode(translated,
                                                 skip_special_tokens=True)[0]
        return translated_text

    print(predict_quantized("我爱ecse484."))
    # print(predict_quantized("我爱ecse484.我爱math."))