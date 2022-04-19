import sys
import argparse
from instance import Instance

class AWSCmd(object):
    def __init__(self):
        pass

    def build_argument_parser(self):
        """Build arguments"""
        help_text = "Specify service type (eg. EC2) followed by action"

        parser = argparse.ArgumentParser()

        actions = parser.add_argument_group("Action", "Start, Stop, Reboot")

        action_args = [("--start", "-b"), ("--stop", "-x"), ("--reboot", "-r")]

        for long_arg, short_arg in action_args:
            actions.add_argument(
                long_arg,
                short_arg,
                default=None,
                help=help_text,
                nargs="+"
            )

        return parser

    def aws_action(self):
        """Helper function for instance actions"""
        args = self.build_argument_parser().parse_args()
        
        if args.start is not None:
            print("Starting instance...")
            instance_type = args.start[0]
            instance_id = args.start[1]
            instance = Instance(instance_type,instance_id)
            instance.start()
        elif args.stop is not None:
            print("Stopping instance...")
            instance_type = args.stop[0]
            instance_id = args.stop[1]
            instance = Instance(instance_type,instance_id)
            instance.stop()
        elif args.reboot is not None:
            print("Rebooting instance...")
            instance_type = args.reboot[0]
            instance_id = args.reboot[1]
            instance = Instance(instance_type,instance_id)
            instance.reboot()
        


def main():

    aws_cmd = AWSCmd()

    if len(sys.argv) > 1:
        aws_cmd.aws_action()
    else:
        print("No arguments given!")
       


if __name__ == "__main__":
    main()
