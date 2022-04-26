import sys
import argparse
import boto3
from instance import Instance


class AWSCmd(object):
    def __init__(self):
        pass

    def build_argument_parser(self):
        """Build arguments"""
        help_text = "Specify service type (eg. EC2) followed by action, for create specify keypair name"

        parser = argparse.ArgumentParser()

        actions = parser.add_argument_group("Action", "Start, Stop, Reboot, Create")

        action_args = [
            ("--start", "-b"),
            ("--stop", "-x"),
            ("--reboot", "-r"),
            ("--create", "-c"),
        ]

        for long_arg, short_arg in action_args:
            actions.add_argument(
                long_arg, short_arg, default=None, help=help_text, nargs="+"
            )

        return parser

    def aws_action(self):
        """Helper function for instance actions"""
        args = self.build_argument_parser().parse_args()

        if args.start is not None:
            print("Starting instance...")
            instance_type = args.start[0]
            instance_id = args.start[1]
            instance = Instance(instance_type, instance_id)
            instance.start()
        elif args.stop is not None:
            print("Stopping instance...")
            instance_type = args.stop[0]
            instance_id = args.stop[1]
            instance = Instance(instance_type, instance_id)
            instance.stop()
        elif args.reboot is not None:
            print("Rebooting instance...")
            instance_type = args.reboot[0]
            instance_id = args.reboot[1]
            instance = Instance(instance_type, instance_id)
            instance.reboot()
        elif args.create is not None:
            instance_type, keypair = args.create[0], args.create[1]
            response = self.create_instance(instance_type, keypair)
            print(response)

    def create_instance(self, instance_type, keypair):
        """Create an EC2 instance"""
        ec2 = boto3.resource(instance_type)
        key = ec2.create_key_pair(KeyName=keypair)

        private_key_file = open("{}.pem".format(keypair), "w")
        private_key_file.write(key.key_material)
        private_key_file.close()

        # shell script to run on start
        user_data = """#!/bin/bash
        yum update -y
        amazon-linux-extras install docker
        service docker start
        systemctl enable docker
        yum install git -y
        git clone https://github.com/jchen42703/chinese-translation-api.git chinese
        cd /chinese/server
        docker build -t chinese_translation_server .
        docker run -d -e ENV_TYPE="production" -e DEPLOY_TYPE="server" --name translation_server_container_deploy -p 80:5001 chinese_translation_server
        """

        instances = ec2.create_instances(
            ImageId="ami-0f9fc25dd2506cf6d",
            MinCount=1,
            MaxCount=1,
            UserData=user_data,
            InstanceType="t2.large",
            KeyName=keypair,
        )

        return instances


def main():

    aws_cmd = AWSCmd()

    if len(sys.argv) > 1:
        aws_cmd.aws_action()
    else:
        print("No arguments given!")


if __name__ == "__main__":
    main()
