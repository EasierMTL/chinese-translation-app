from fastapi import APIRouter
from api.routes import translate

router = APIRouter()
router.include_router(translate.router, tags=["translate-chinese"])
