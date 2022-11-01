# Deploying and Benchmarking with Terraform and Locust

The server docker image URI to load-test: `public.ecr.aws/h1c6y7g8/chinese-translation-api:latest`

## Deploy API Server with Terraform

Make sure you have `terraform` installed and `aws` CLI configured.

- Feel free to change the `key_name` to the correct SSH key name that you want to ssh with.

```bash
cd server
terraform init
terraform plan
terraform apply
```

Clean up with:

```bash
terraform destroy
```

## To-Do for Next Time

- Check if need to setup nginx as well
  - Try to automatically set that up if possible