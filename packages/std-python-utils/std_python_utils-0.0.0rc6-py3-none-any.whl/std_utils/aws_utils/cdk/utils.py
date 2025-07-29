import boto3
from aws_cdk import Environment


def get_environment() -> Environment:
    session = boto3.Session()

    return Environment(
        account=session.client('sts').get_caller_identity()['Account'], region=boto3.session.Session().region_name
    )
