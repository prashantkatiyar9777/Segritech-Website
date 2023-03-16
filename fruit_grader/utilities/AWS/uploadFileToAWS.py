import boto3
from botocore.exceptions import ClientError
import logging

from cryptography.fernet import Fernet
from .credentials import *

# initialize the Fernet class
key = b'67OKbflvzdIwv6Jzu4GzeghGaV_DsTXPvrFCOzPAgrk='
f = Fernet(key)


def upload_file_to_aws(local_file, bucket, s3_file):

    s3 = boto3.client(
            's3',
            aws_access_key_id = f.decrypt(AWS_ACCESS_KEY_ID).decode(),
            aws_secret_access_key = f.decrypt(AWS_SECRET_ACCESS_KEY).decode(),
        )

    try:
        s3.upload_file(local_file, bucket, s3_file)
    except ClientError as e:
        logging.error(e)
