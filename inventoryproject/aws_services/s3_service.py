import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

def upload_file_to_s3(file_name, bucket_name, object_name=None):
    """Upload a file to an S3 bucket."""
    if object_name is None:
        object_name = file_name
    
    try:
        s3.upload_file(file_name, bucket_name, object_name)
        print(f"File {file_name} uploaded to {bucket_name}/{object_name}.")
    except ClientError as e:
        print(f"Error uploading file: {e}")

def list_files_in_bucket(bucket_name):
    """List files in an S3 bucket."""
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        files = [content['Key'] for content in response.get('Contents', [])]
        return files
    except ClientError as e:
        print(f"Error listing files: {e}")
        return []

def download_file_from_s3(bucket_name, object_name, file_name):
    """Download a file from S3."""
    try:
        s3.download_file(bucket_name, object_name, file_name)
        print(f"File {object_name} downloaded to {file_name}.")
    except ClientError as e:
        print(f"Error downloading file: {e}")
