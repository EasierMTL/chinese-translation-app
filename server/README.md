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

## Build and Push to ECR

```bash
poetry export -f requirements.txt --output requirements.txt
```

Build docker:

```bash
docker build -t chinese-translation-api .
```

Push to ECR:

```bash
# authenticate
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/h1c6y7g8

# tag as latest and push
# Remember to increment the version
docker tag chinese-translation-api:latest public.ecr.aws/h1c6y7g8/chinese-translation-api:v0.0.2
docker push public.ecr.aws/h1c6y7g8/chinese-translation-api:v0.0.2
```

Run the docker image as container:

```bash
# regular
docker run -d --name translation_server_container -p 5001:5001 chinese-translation-api

# with env
docker run -e ENV_TYPE="production" -e DEPLOY_TYPE="server" --name translation_server_container_deploy -p 5001:5001 -d chinese-translation-api
```

## Docker Releases

- `v0.0.1`: Basic.
