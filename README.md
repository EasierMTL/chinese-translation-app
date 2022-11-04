# Chinese Translation Web App

- [Frontend](./frontend)
- [Python](./server)
  - [Backend REST API](./server/chinese_translation_api)
  - [Load-Testing CLI](./server/loadtest_cli)
- [AWS/Terraform Deployments](./deploy)
- [Misc. Documentation](./docs)

## Getting Started

See the individual READMEs in `frontend` and `server`.

## Build

```bash
# for building repeatedly when debugging
docker-compose build --no-cache

# running
docker-compose up -d
```
