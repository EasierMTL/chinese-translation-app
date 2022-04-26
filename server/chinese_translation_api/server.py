"""The server entrypoint
"""
import os
from typing import List
from fastapi import FastAPI
import torch
from fastapi.middleware.cors import CORSMiddleware
from chinese_translation_api.routes import router

torch.set_num_threads(1)


def get_origins() -> List[str]:
    """configures cors based on the environment
    """
    env = os.environ.get("ENV_TYPE")
    is_prod = env == "production"

    if is_prod:
        origins = [
            "https://chinesetranslationapi.com/",
            "http://localhost:3006",
        ]
    else:
        origins = [
            "http://localhost", "http://localhost:3006", "http://localhost:3000"
        ]
    print("origins: ", origins)
    return origins


def get_application(api_prefix: str) -> FastAPI:
    """Actually creates the FastAPI app
    From:
    https://github.com/nsidnev/fastapi-realworld-example-app/blob/master/app/main.py
    """

    application = FastAPI()

    deploy_type = os.environ.get("DEPLOY_TYPE")
    # Only add cors when we're deploying on an app
    if deploy_type != "server":
        application.add_middleware(
            CORSMiddleware,
            allow_origins=get_origins(),
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    application.include_router(router.router, prefix=api_prefix)

    return application


app = get_application("/api")
