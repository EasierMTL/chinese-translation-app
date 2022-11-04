# API

```
# https://stackoverflow.com/questions/59882884/vscode-doesnt-show-poetry-virtualenvs-in-select-interpreter-option

poetry config virtualenvs.in-project true

# shows the name of the current environment
poetry env list

poetry install
```

## Getting Started

To start the api:

```bash
# Regular model
poetry run uvicorn chinese_translation_api.server:app --workers 1 --reload --port=5001

# Quantized
MODEL_TYPE=quantized_dynamic DEPLOY_TYPE=server poetry run uvicorn chinese_translation_api.server:app --workers 1 --reload --port=5001
```

## Build

```
poetry export -f requirements.txt --output requirements.txt
```

Build docker:

```
docker build -t chinese_translation_server .
```

Run docker:

```bash
# regular
docker run -d --name translation_server_container -p 5001:5001 chinese_translation_server

# with env
docker build -t chinese_translation_server . && docker run -e ENV_TYPE="production" -e DEPLOY_TYPE="server" --name translation_server_container_deploy -p 5001:5001 -d chinese_translation_server
```
