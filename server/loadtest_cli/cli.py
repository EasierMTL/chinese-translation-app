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


def main():
    """The main function to run the CLI.
    """
    cli = LoadTestCLI()
    config_fpath = cli.get_config_fpath()
    print(f"Using config: {config_fpath}")
    config = cli.parse_config(config_path=config_fpath)

    # Workflow
    # 1. Start instance with terraform.
    # 2. Locust test it
    # 3. Write out information to logs
    # 4. Terraform destroy to clean everything up.


if __name__ == "__main__":
    main()