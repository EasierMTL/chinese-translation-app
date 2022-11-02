import yaml
import os
import argparse


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
    repo_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    # Path to the terraform deployment directory
    terraform_dir = os.path.join(repo_path, "deploy", "server")

    # Start instance to loadtest with Terraform
    os.chdir(terraform_dir)
    os.system("terraform init")

    apply_cmd = cli.build_terraform_apply_cmd(config)
    os.system(apply_cmd)

    # Load test with Locust

    # Clean up
    os.system("terraform destroy -auto-approve")


if __name__ == "__main__":
    main()