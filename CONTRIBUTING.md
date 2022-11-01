# Contributor Guidelines and Documentation

## Upload to the ECR

Run these commands if you want to upload a new docker image to the ECR. Make sure you already have the `aws` CLI installled and configured (`aws configure`).

```bash
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/h1c6y7g8
```

For the server docker image, build, tag, and push the container with:

```bash
cd server
docker build -t chinese_translation_server .
docker tag chinese_translation_server:latest public.ecr.aws/h1c6y7g8/chinese-translation-api:latest
docker push public.ecr.aws/h1c6y7g8/chinese-translation-api:latest
```

For the time being, we're not uploading the UI docker image or the combined docker image, since we're only load testing the API.
