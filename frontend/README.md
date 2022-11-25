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
yarn start
```

If you are testing functionality, make sure you are concurrently running the backend with the `DEPLOY_TYPE` equal to anything **besides** `server`.

## Build and Run With Docker

To build:

```bash
docker build -t jchen42703/ch-tl-ui:latest .
```

To run:

```bash
docker run -d --name translation_container -p 3006:3006 jchen42703/ch-tl-ui:latest
```

To publish:

```bash
docker push jchen42703/ch-tl-ui:latest
```
