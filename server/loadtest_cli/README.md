# Load Test CLI

Run the CLI to automatically deploy the API on an AWS instance with Docker/Terraform and load test the API with Locust.

## Getting Started

```bash
# Call python to run cli.py and specify the config.yaml path
python ./cli.py -c ./config.yaml
```

This will start the AWS instance and load test it with the settings defined in [`config.yaml`](./config.yaml)

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
