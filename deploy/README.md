# Deploying and Benchmarking with Terraform and Locust

The server docker image URI to load-test: `public.ecr.aws/h1c6y7g8/chinese-translation-api:latest`

## Deploy API Server with Terraform

Make sure you have `terraform`, `gcloud`, and `aws` already installed and configured.

- For `gcloud`, make sure to have already run `gcloud init`
- For `aws`, make sure to have already run `aws init`

**AWS Only**

- Feel free to change the `key_name` in `variables.tf` to the correct SSH key name that you want to ssh with.

**Deploy with Terraform:**

```bash
cd server
terraform init
terraform plan

# For quantized
terraform apply -var use_quantized=1
# For regular
terraform apply
```

Clean up with:

```bash
terraform destroy
```

# Misc. Notes

## AWS

- The startup script logs located @ `/var/log/cloud-init-output.log`

## GCE

- The startup script takes around `1m48.555s`
- Startup script logs located @ `/var/log/daemon.log`
  - https://stackoverflow.com/questions/42786661/startup-script-logs-location
