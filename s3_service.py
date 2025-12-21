import boto3
from botocore.exceptions import NoCredentialsError
import uuid

S3_BUCKET_NAME = "bucket1-miproyecto"

s3_client = boto3.client("s3")  # usa IAM Role automáticamente


def upload_file_to_s3(file, filename, content_type):
    unique_filename = f"{uuid.uuid4()}_{filename}"

    s3_client.upload_fileobj(
        file,
        S3_BUCKET_NAME,
        unique_filename,
        ExtraArgs={"ContentType": content_type}
    )

    return unique_filename
