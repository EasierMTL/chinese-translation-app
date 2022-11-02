"""Base translator classes.
"""
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class Predictor:
    def predict(self, message: str) -> str:
        raise NotImplementedError()


class ChineseToEnglishTranslator(Predictor):
    """Inference object for chinese to english translation."""

    def __init__(self, model_path: str = None):
        # English to Chinese: https://huggingface.co/Helsinki-NLP/opus-mt-en-zh
        self.tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-zh-en")

        if model_path is None:
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                "Helsinki-NLP/opus-mt-zh-en"
            )
            print("Loaded default model")
        else:
            self.model = torch.load(model_path)

    def predict(self, message):
        """Runs the prediction pipeline."""
        inputs = self.tokenizer(message, return_tensors="pt")
        translated = self.model.generate(**inputs)
        translated_text = self.tokenizer.batch_decode(
            translated, skip_special_tokens=True
        )[0]
        return translated_text


class EnglishToChineseTranslator(Predictor):
    """English to Chinese Translator"""

    def __init__(self, model_path: str = None):
        # English to Chinese: https://huggingface.co/Helsinki-NLP/opus-mt-en-zh
        self.tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-zh")

        if model_path == None:
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                "Helsinki-NLP/opus-mt-en-zh"
            )
        else:
            self.model = torch.load(model_path)

    def predict(self, message):
        """Runs the prediction pipeline."""
        inputs = self.tokenizer(message, return_tensors="pt")
        translated = self.model.generate(**inputs)
        translated_text = self.tokenizer.batch_decode(
            translated, skip_special_tokens=True
        )[0]
        return translated_text
