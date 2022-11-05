import yaml
import os
import argparse
import json
import time
import requests


def check_if_ready(api_url: str) -> bool:
    """Checks if API is ready to accept connections and requests.

    Sends GET requests until one goes through and a connection is established.
    The response status does not matter, only if we can establish a connection,
    and get a response.
    """
    try:
        resp = requests.get(api_url, timeout=3)
        # Bad Gateway --> NGINX deployed, but API still not ready
        is_bad_gateway = resp.status_code == 502
        if is_bad_gateway:
            return False

        # Ideally, should be 200 or 405, but can depend on your API.
        return True
    except:
        return False


class LoadTestCLI(object):
    """The main function to manage the CLI.
    """

    def get_config_fpath(self):
        parser = argparse.ArgumentParser(
            prog='loadtest',
            description='CLI for load test cloud deployments of the core API',
        )
        parser.add_argument('-c',
                            '--config',
                            nargs=1,
                            required=True,
                            help="Path to the config.")
        args = parser.parse_args()
        return args.config[0]

    def parse_config(self, config_path: str):
        """Build arguments from the local config.
        """
        # Read YAML file
        with open(config_path, 'r', encoding="utf-8") as stream:
            data_loaded = yaml.safe_load(stream)
        return data_loaded

    def build_terraform_apply_cmd(self, config):
        """Builds the Terraform apply command, which deploys the API on to the
        desied cloud provider.
        """
        use_quantized_cmd = "-var='use_quantized=1'" if config[
            "model_type"] == "quantized" else ""
        key_name = config["ssh_key_name"]
        key_name_cmd = f"-var='key_name={key_name}'"
        instance_type = config["instance_type"]
        instance_type_cmd = f"-var='instance_type={instance_type}'"
        base_cmd = "terraform apply -auto-approve"
        # Add all of the Terraform variable overwrites
        for cmd in [use_quantized_cmd, key_name_cmd, instance_type_cmd]:
            base_cmd += f" {cmd}"
        return base_cmd

    def create_instance(self, config: dict):
        """Initializes Terraform and runs Terraform to create the cloud
        instances to load-test.
        """
        os.system("terraform init")
        apply_cmd = self.build_terraform_apply_cmd(config)
        os.system(apply_cmd)

    def get_instance_ip(self):
        """Gets the instance IP from the Terraform state.

        This command should be run after `terraform apply` has been run.
        """
        output = os.popen("terraform output -json").read()
        parsed = json.loads(output)
        if not isinstance(parsed, dict):
            raise ValueError(
                f"terraform output should be a map but is: {type(parsed)}, {parsed}"
            )

        ip_map = parsed.get("public_ip", "")
        if ip_map == "":
            raise ValueError(
                f"terraform output missing map 'public_ip': {parsed}")
        return ip_map["value"]

    def create_loadtest_url(self, ip: str):
        """Creates the HTTP url to load-test from the IP address.
        """
        return f"http://{ip}/"

    def load_test(self, url: str, locust_file_path: str, log_path: str,
                  config: dict):
        """Runs the Locust load-testing according to the user's config.

        Load-tests through the locust CLI instead of with the library to allow
        for multiple workers.

        ```python
        import gevent
        from locust.env import Environment
        from .locustfile import TranslateUser
        from locust.stats import stats_printer, stats_history

        # setup Environment and Runner
        env = Environment(user_classes=[TranslateUser])
        env.create_local_runner()
        # start a greenlet that periodically outputs the current stats
        gevent.spawn(stats_printer(env.stats))
        # start a greenlet that save current stats to history
        gevent.spawn(stats_history, env.runner)
        env.runner.start(num_users, spawn_rate=user_spawn_rate)

        # in 60 seconds stop the runner
        gevent.spawn_later(test_runtime, lambda: env.runner.quit())

        # wait for the greenlets
        env.runner.greenlet.join()
        ```         
        """
        url = url + "/" if not url.endswith("/") else url
        # Example:
        # locust -f locustfile.py --host=http://127.0.0.1:5001/ --headless -u 1 -r 1 --run-time 5s --expect-workers=1 --logfile="./locust.log"
        num_users, user_spawn_rate = config["users"], config["spawn_rate"]
        test_runtime = config["run_time"]
        workers = config["expect_workers"]
        os.system(
            f"locust -f {locust_file_path} --headless --host={url} --csv=load_test -u {num_users} -r {user_spawn_rate} --run-time {test_runtime} --expect-workers={workers} --logfile={log_path}"
        )

        return

    def wait_until_ready(self, host: str, timeout_sec=30, retry_delay_sec=2):
        """
        Pings host until we receive a valid response or it takes too long and
        we time out.

        Returns:
            True if ping was eventually successful.
            False if timed out.
        """
        current_time_sec = time.time()
        timeout_time_sec = current_time_sec + timeout_sec
        server_is_up = check_if_ready(host)
        while current_time_sec < timeout_time_sec and not server_is_up:
            time.sleep(retry_delay_sec)
            current_time_sec = time.time()
            server_is_up = check_if_ready(host)

        return server_is_up


def main():
    """The main function to run the CLI.

    Workflow
    1. Start instance with Terraform.
    2. Load test with Locust.
    3. Write out information to logs
    4. Terraform destroy to clean everything up.
    """
    cli = LoadTestCLI()
    config_fpath = cli.get_config_fpath()
    config = cli.parse_config(config_path=config_fpath)
    print(f"Using config [{config_fpath}]:\n{config}")

    # absolute path to the repo root dir
    file_path = os.path.abspath(__file__)
    cli_path = os.path.dirname(file_path)
    repo_path = os.path.dirname(os.path.dirname(os.path.dirname(file_path)))
    # Path to the terraform deployment directory
    terraform_dir = os.path.join(repo_path, "deploy", "server")

    # Start instance to loadtest with Terraform
    os.chdir(terraform_dir)  # must be in directory with terraform files
    cli.create_instance(config)

    ip = cli.get_instance_ip()
    loadtest_url = cli.create_loadtest_url(ip)

    print("Waiting until instance is ready to receive API requests...")
    os.chdir(os.path.join(cli_path,
                          "stats"))  # Chdir so csv files save in the stats dir
    # Normally takes 130-140 seconds to completely initialize the instance's API
    timeout_sec = 140
    translation_url = f"{loadtest_url}/api/translate/chinese"
    is_ready = cli.wait_until_ready(translation_url, timeout_sec, 2)
    if is_ready:
        # Load test with Locust
        log_path = os.path.join(cli_path, "locust.log")
        locust_file_path = os.path.join(cli_path, "locustfile.py")
        print(f"\nLoad-testing: {loadtest_url}\nLogging to: {log_path}\n")
        cli.load_test(loadtest_url, locust_file_path, log_path, config)
    else:
        print(
            f"ERROR: API not ready after {timeout_sec} seconds, could not load-test."
        )

    # Clean up
    os.chdir(terraform_dir)  # must be in directory with terraform files
    print("Cleaning up...")
    os.system("terraform destroy -auto-approve")


if __name__ == "__main__":
    main()