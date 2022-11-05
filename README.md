# Chinese Translation Web App

Full-stack web application to automatically translate Chinese to English (and vice-versa) with React/FastAPI.

## Table of Contents

- [Frontend](./frontend)
- [Python](./server)
  - [Backend REST API](./server/README.md)
  - [Model Development](./server/chinese_translation_api/models/README.md)
  - [Model Evaluation Pipeline](./server/chinese_translation_api/evaluation)
  - [Load-Testing CLI](./server/loadtest_cli/README.md)
- [AWS/Terraform Deployment Configurations and Scripts](./deploy/README.md)
- [Misc. Documentation](./docs/deployment.md)

## Getting Started

To build the full web-app and run it:

```bash
# for building repeatedly when debugging
docker-compose build --no-cache

# running
docker-compose up -d
```

If you don't want to use `docker` or want to debug, run the `frontend` and `server` separately. See the individual READMEs in `frontend` and `server` for more information.
