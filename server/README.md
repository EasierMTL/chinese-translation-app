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
poetry run uvicorn api.server:app --workers 1 --reload
```
