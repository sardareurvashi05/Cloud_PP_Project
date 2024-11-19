import boto3
from botocore.exceptions import ClientError
from django.conf import settings
import boto3

def get_s3_client():
    return boto3.client('s3', region_name=settings.AWS_S3_REGION_NAME)

def upload_image_with_metadata_1(file_path, bucket_name, key):
    s3 = get_s3_client()

    try:
        with open(file_path, 'rb') as file_data:
            s3.upload_fileobj(
                file_data,
                bucket_name,
                key,
                ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/jpeg'}
            )
        print(f"Image uploaded to S3 with key {key}")
    except ClientError as e:
        print(f"Error uploading file to S3: {e}")
        raise e

def upload_image_with_metadata(file_path, bucket_name, key):
    s3_client = boto3.client('s3', region_name=settings.AWS_S3_REGION_NAME)
    try:
        s3_client.upload_file(
            file_path,
            bucket_name,
            key,
            ExtraArgs={'ACL': 'public-read'}
        )
    except Exception as e:
        raise ValueError(f"Failed to upload to S3: {str(e)}")
