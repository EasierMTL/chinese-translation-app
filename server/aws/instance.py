from botocore.exceptions import ClientError
import boto3


# Deployment of docker with AWS
# https://github.com/AlexIoannides/py-docker-aws-example-project/blob/master/deploy_to_aws.py


class Instance:

    """Control AWS EC2 instances"""

    def __init__(self, instance_type, instance_id):
        self.ec2 = boto3.client(instance_type)
        self.instance_id = instance_id

    def reboot(self):
        """Reboot EC2 instance"""
        try:
            res = self.ec2.reboot_instances(InstanceIds=[self.instance_id])
            print("Rebooted instance!", res)
        except ClientError as e:
            print(e.response["Error"]["Message"])

    def start(self):
        """Start EC2 instance"""
        try:
            res = self.ec2.start_instances(
                InstanceIds=[self.instance_id], AdditionalInfo="string"
            )
            print("Starting Instance!", res)
        except ClientError as e:
            print(e.response["Error"]["Message"])

    def stop(self):
        """Stop EC2 instance"""
        try:
            res = self.ec2.stop_instances(InstanceIds=[self.instance_id])
            print("Stopping Instance!", res)
        except ClientError as e:
            print(e.response["Error"]["Message"])
