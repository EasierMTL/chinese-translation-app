# Load Test CLI

Run the CLI to automatically deploy the API on an AWS instance with Docker/Terraform and load test the API with Locust.

This is intended so you can test the same API across multiple instance types to identify the optimal instance type to use for your userbase.

## Getting Started

```bash
# Call python to run cli.py and specify the config.yaml path
python ./cli.py -c ./config.yaml
```

This will create and start the AWS instance and load test it with the settings defined in [`config.yaml`](./config.yaml)

## How Does the CLI Work?

The CLI is a simple wrapper around Locust and Terraform. It goes through the following steps:

1. Parses configuration.
2. Starts an AWS instance based on the config with Terraform.
3. Waits until the instance is ready for load testing.
4. Load tests with Locust according to the provided config.
5. Writes stats and logs to files relative to this directory.
6. Clean up the created AWS resources and instances with Terraform (`terraform destroy`).

This means that if you cancel the CLI midway, you could run into a scenario where resources are not cleaned up properly. **If you do `CTRL + C` during load testing, it will cancel load testing and go straight to Terraform cleanup steps.**

If that still does not work, you could manually `cd` into `deploy/server` and call the `terraform destroy` command yourself.

## Load-Testing without CLI

You can also run the Locust file locally:

```bash
# in this directory
locust
```

Or, you can locust headless:

```bash
# For local testing, we use localhost and make sure it has the forward slash

# For testing:
locust -f locustfile.py --host=http://127.0.0.1:5001/ --headless -u 1 -r 1 --run-time 5s --expect-workers=1

# For more realistic testing:
locust -f locustfile.py --host=http://127.0.0.1:5001/ --headless -u 100 -r 10 --run-time 30s --expect-workers=2

# Logging to file
locust -f locustfile.py --host=http://127.0.0.1:5001/ --headless -u 1 -r 1 --run-time 5s --expect-workers=1 --logfile="./locust.log"
```
