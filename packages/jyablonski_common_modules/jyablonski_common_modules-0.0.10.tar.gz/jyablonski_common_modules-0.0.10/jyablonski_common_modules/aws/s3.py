import logging

import botocore

from .exceptions import S3PrefixCheckFail


logger = logging.getLogger(__name__)

def check_s3_file_exists(client: botocore.client, bucket: str, file_prefix: str):
    """
    Function to check if a file exists in an S3 Bucket.

    Args:
        client (S3 Client) - Boto3 S3 Client Object

        bucket (str) - Name of the S3 Bucket (`jyablonski-dev`)

        file_prefix (str) - Name of the S3 File (`tables/my-table/my-table-2023-05-25.parquet`)

    Returns:
        None, but will raise an error if the file doesn't exist.
    """
    result = client.list_objects_v2(Bucket=bucket, Prefix=file_prefix, MaxKeys=1,)
    if "Contents" in result.keys():
        logging.info(f"S3 File Exists for {bucket}/{file_prefix}")
    else:
        raise S3PrefixCheckFail(f"S3 Prefix for {bucket}/{file_prefix} doesn't exist")
