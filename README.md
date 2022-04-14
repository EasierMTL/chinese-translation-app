# Chinese Translation API

## Getting Started

To run the backend, do:

```
cd server
poetry config virtualenvs.in-project true
poetry install
poetry run gunicorn api.server:app --workers 2
```
