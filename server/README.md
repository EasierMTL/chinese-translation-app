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

```
poetry run uvicorn api.server:app --workers 1 --reload --port=5000
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

```
docker run -d --name translation_server_container -p 8000:5001 chinese_translation_server
```
