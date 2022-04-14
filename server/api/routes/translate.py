"""The main endpoint that will be tested
"""

from starlette.responses import JSONResponse
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter()


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


class ChineseTextToTranslateReq(BaseModel):
    text: str

    class Config:
        """example docs"""
        schema_extra = {"example": {"text": "我爱ECSE484"}}


zh_translator = ChineseToEnglishTranslator()


@router.post("/translate/chinese")
async def run_prediction(req: ChineseTextToTranslateReq) -> JSONResponse:
    """Runs the model prediction
    """
    prediction = zh_translator.predict(req.text)
    return {'prediction': prediction}


class EnglishToChineseTranslator(object):
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


class EnglishToChineseTranslateReq(BaseModel):
    """English to chinese translation JSON body
    """
    text: str

    class Config:
        """example docs"""
        schema_extra = {"example": {"text": "I love ECSE 484"}}


en_translator = EnglishToChineseTranslator()


@router.post("/translate/english")
async def run_english_to_chinese_pred(
        req: EnglishToChineseTranslateReq) -> JSONResponse:
    """Runs the model prediction
    """
    prediction = en_translator.predict(req.text)
    return {'prediction': prediction}