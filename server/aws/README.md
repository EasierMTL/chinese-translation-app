# Getting Started

1. Make sure you have an IAM user with enough permissions. For example, for EC2 you can just attach the existing policy `AmazonEC2FullAccess`. Refer to [this](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console) on how to setup IAM user.

Store your `ACCESS_KEY_ID` and `SECRET_ACCESS_KEY` in a safe place.

2. Make sure to install `AWS CLI` if you don't have it already. Then run `aws configure`, you should have something like this (replace them with your own values):

[AWS CLI Setup](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)

```
$ aws configure
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-west-2
Default output format [None]: json

```

# Using the CLI

The CLI allows you to start, stop, and reboot. You need to specify `instance_type` (eg. EC2) followed by the `instance_id` associated with it.

Start instance:

`python3 aws_cmd.py -b instance_type instance_id`

Stop instance:

`python3 aws_cmd.py -x instance_type instance_id`

Reboot instance:

`python3 aws_cmd.py -r instance_type instance_id`

If you run into any errors, make sure you have enough permissions for your IAM user, double check your `instance_id` and that its the correct `instance_type`.
