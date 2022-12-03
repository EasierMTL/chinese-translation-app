# Frontend

Contains text editors (`draft.js`) to allow users to type in words and get translations back. **API requests are debounced** to prevent huge surges of requests.

![](docs_assets/demo.png)

## Getting Started

To install dependencies:

```bash
yarn install
```

To run the frontend for development:

```bash
yarn dev
```

If you are testing functionality, make sure you are concurrently running the backend with the `DEPLOY_TYPE` equal to anything **besides** `server`.

## Build and Run With Docker

To build:

```bash
docker build -t jchen42703/ch-tl-ui:latest .
```

To run:

```bash
docker run -p 3006:3006 jchen42703/ch-tl-ui:latest
```

To build and publish to Docker Hub:

```bash
# Remember to rebuild before you push a new version!
docker build -t jchen42703/ch-tl-ui:latest .
UI_VERSION=$(node -p -e "require('./package.json').version")
PUSH_REPO="jchen42703/ch-tl-ui:v${UI_VERSION}"
docker tag jchen42703/ch-tl-ui:latest $PUSH_REPO
docker push $PUSH_REPO
```
