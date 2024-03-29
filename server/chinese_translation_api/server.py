"""The server entrypoint
"""
import os
from typing import List
from fastapi import FastAPI
import torch
from fastapi.middleware.cors import CORSMiddleware
from chinese_translation_api.routes import router

torch.set_num_threads(1)

API_VERSION = "v0.0.4"


def get_origins() -> List[str]:
    """configures cors based on the environment
    """
    env = os.environ.get("ENV_TYPE")
    is_prod = env == "production"
    domain = os.environ.get("CLIENT_DOMAIN")
    if is_prod:
        origins = [
            "http://localhost:3006",
        ]
        # Whitelist the HTTP and HTTPS versions of the domain if available
        if domain is not None:
            origins.append(f"http://{domain}/")
            origins.append(f"https://{domain}/")
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
    # Print environment
    print(f"API_VERSION: {API_VERSION}")
    env_vars = [
        "DEPLOY_TYPE", "ENV_TYPE", "NUM_WORKERS", "MODEL_TYPE", "CLIENT_DOMAIN",
        "NO_PREPEND"
    ]
    for env_var in env_vars:
        print(f"{env_var}: {os.environ.get(env_var)}")
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


# Serving on K8s doesn't let you proxy_pass the traditional way.
if os.environ.get("NO_PREPEND"):
    app = get_application("")
else:
    app = get_application("/api")
