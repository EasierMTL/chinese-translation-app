"""The main endpoint that will be tested
"""

from starlette.responses import JSONResponse
from pydantic import BaseModel
from fastapi import APIRouter
import os
from api.models.base import ChineseToEnglishTranslator, EnglishToChineseTranslator

router = APIRouter()


class ChineseTextToTranslateReq(BaseModel):
    """Chinese to english  translation request body
    """
    text: str

    class Config:
        """example docs"""
        schema_extra = {"example": {"text": "我爱ECSE484"}}


zh_translator = ChineseToEnglishTranslator()


@router.post("/translate/chinese")
async def run_prediction(req: ChineseTextToTranslateReq) -> JSONResponse:
    """Runs the model prediction
    """
    print(req)
    prediction = zh_translator.predict(req.text)
    return {'prediction': prediction}


deploy_type = os.environ.get("DEPLOY_TYPE")

if deploy_type != "server":

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
