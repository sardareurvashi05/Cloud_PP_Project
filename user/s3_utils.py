import boto3
from botocore.exceptions import ClientError
from django.conf import settings

def get_s3_client():
    return boto3.client('s3', region_name=settings.AWS_S3_REGION_NAME)

def upload_to_s3(file, username):
    s3 = get_s3_client()

    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    file_key = f"media/profile_pictures/{username}.jpg"

    if not bucket_name:
        raise ValueError("Bucket name is not set in settings.")

    try:
        # Set the correct content type
        content_type = file.content_type if hasattr(file, 'content_type') else 'application/octet-stream'
        s3.upload_fileobj(file, bucket_name, file_key,ExtraArgs={'ContentType': content_type})
        file_url = f"https://{bucket_name}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{file_key}"
        return file_url
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
        return None
        
def generate_presigned_url(bucket_name, key, expiration=3600):
    """Generate a pre-signed URL to access the file."""
    s3_client = get_s3_client()
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': key},
            ExpiresIn=expiration
        )
        #print(f"Pre-signed URL: {response}")
        return response
    except ClientError as e:
        print(f"Error generating pre-signed URL: {e.response['Error']['Message']}")
        return None

def get_profile_picture(file_name):
    """Generate the pre-signed URL for the user's profile picture."""
    key = f"{settings.AWS_LOCATION}/{file_name}"
    #key = f"media/profile_pictures/urvashi.jpg"
    return generate_presigned_url(settings.AWS_STORAGE_BUCKET_NAME, key)