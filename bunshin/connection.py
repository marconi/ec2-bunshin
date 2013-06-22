from boto import ec2

from .config import AWS_ACCESS_KEY, AWS_SECRET_KEY


def connect_to_region(region_name):
    """ Connect to an AWS region. """
    return ec2.connect_to_region(region_name=region_name,
                                 aws_access_key_id=AWS_ACCESS_KEY,
                                 aws_secret_access_key=AWS_SECRET_KEY)
