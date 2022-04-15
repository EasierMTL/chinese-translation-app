import boto3
import os
from botocore.exceptions import ClientError

INSTANCE_ID = os.environ.get("INSTANCE_ID")

# Deployment of docker with AWS 
# https://github.com/AlexIoannides/py-docker-aws-example-project/blob/master/deploy_to_aws.py

class Instances():

    """ Control AWS EC2 instances
    """
    def __init__(self):
        self.ec2 = boto3.client('ec2')

    def reboot(self):
        """ Reboot EC2 instance
        """
        try:
            res = self.ec2.reboot_instances(InstanceIds=[INSTANCE_ID])
            print("Rebooted instance!", res)
        except ClientError as e:
            print(e.response['Error']['Message'])

    def start(self):
        """ Start EC2 instance
        """
        try:
            res = self.ec2.start_instances(InstanceIds=[INSTANCE_ID], AdditionalInfo='string')
            print("Starting Instance!", res)
        except ClientError as e:
            print(e.response['Error']['Message'])

    def stop(self):
        """ Stop EC2 instance
        """
        try:
            res= self.ec2.stop_instances(InstanceIds=[INSTANCE_ID])
            print("Stopping Instance!", res)
        except ClientError as e:
            print(e.response['Error']['Message'])