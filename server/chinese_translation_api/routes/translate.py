"""The main endpoint(s) that will be tested
"""
import os

from starlette.responses import JSONResponse
from pydantic import BaseModel
from fastapi import APIRouter
from chinese_translation_api.models.base import (
    ChineseToEnglishTranslator,
    EnglishToChineseTranslator,
)
from chinese_translation_api.models.load import download_model, model_params


def create_translator_router(deploy_type: str = "server",
                             model_type: str = None):

    class ChineseTextToTranslateReq(BaseModel):
        """Chinese to english  translation request body"""

        text: str

        class Config:
            """example docs"""

            schema_extra = {"example": {"text": "我爱ECSE484"}}

    router = APIRouter()
    model_path = None if model_type is None else model_params[model_type][
        "save_path"]
    if model_type is not None:
        # Download model if doesn't exist
        if not os.path.isfile(model_path):
            download_model(model_path, model_params[model_type]["file_id"])
    zh_translator = ChineseToEnglishTranslator(model_path)

    @router.post("/translate/chinese")
    async def run_prediction(req: ChineseTextToTranslateReq) -> JSONResponse:
        """Runs the model prediction"""
        print(req)
        prediction = zh_translator.predict(req.text)
        return {"prediction": prediction}

    if deploy_type != "server":

        class EnglishToChineseTranslateReq(BaseModel):
            """English to chinese translation JSON body"""

            text: str

            class Config:
                """example docs"""

                schema_extra = {"example": {"text": "I love ECSE 484"}}

        en_translator = EnglishToChineseTranslator()

        @router.post("/translate/english")
        async def run_english_to_chinese_pred(
            req: EnglishToChineseTranslateReq,) -> JSONResponse:
            """Runs the model prediction"""
            prediction = en_translator.predict(req.text)
            return {"prediction": prediction}

    return router
