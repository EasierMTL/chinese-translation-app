from fastapi import APIRouter
import os
from chinese_translation_api.routes import translate

router = APIRouter()

# Environment variables for deployment settings
deploy_type = os.environ.get("DEPLOY_TYPE")
model_type = os.environ.get("MODEL_TYPE")

translate_router = translate.create_translator_router(deploy_type, model_type)
router.include_router(translate_router, tags=["translate-chinese"])
