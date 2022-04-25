"""Base models with no optimization applied.
"""
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class ChineseToEnglishTranslator(object):
    """Template inference object
    """

    def __init__(self):
        # English to Chinese: https://huggingface.co/Helsinki-NLP/opus-mt-en-zh
        self.tokenizer = AutoTokenizer.from_pretrained(
            "Helsinki-NLP/opus-mt-zh-en")

        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            "Helsinki-NLP/opus-mt-zh-en")

    def predict(self, message):
        """Runs the prediction pipeline.
        """
        inputs = self.tokenizer(message, return_tensors="pt")
        translated = self.model.generate(**inputs)
        translated_text = self.tokenizer.batch_decode(
            translated, skip_special_tokens=True)[0]
        return translated_text


class EnglishToChineseTranslator:
    """English to Chinese Translator
    """

    def __init__(self):
        # English to Chinese: https://huggingface.co/Helsinki-NLP/opus-mt-en-zh
        self.tokenizer = AutoTokenizer.from_pretrained(
            "Helsinki-NLP/opus-mt-en-zh")

        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            "Helsinki-NLP/opus-mt-en-zh")

    def predict(self, message):
        """Runs the prediction pipeline.
        """
        inputs = self.tokenizer(message, return_tensors="pt")
        translated = self.model.generate(**inputs)
        translated_text = self.tokenizer.batch_decode(
            translated, skip_special_tokens=True)[0]
        return translated_text