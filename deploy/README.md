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

## GCE

- Make sure `gcloud` is properly configured for `terraform` (`gcloud init`)!
- The startup script takes around `1m48.555s`
- Startup script logs located @ `/var/log/daemon.log`
  - https://stackoverflow.com/questions/42786661/startup-script-logs-location
