import os
import django
import boto3
from botocore.exceptions import ClientError
from django.conf import settings
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventoryproject.settings')
django.setup()

def get_s3_client():
    return boto3.client('s3', region_name=settings.AWS_S3_REGION_NAME)

def create_s3_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region."""
    try:
        s3 = boto3.client('s3', region_name=region)
        
        if region == 'us-east-1' or region is None:
            # No LocationConstraint for us-east-1
            s3.create_bucket(Bucket=bucket_name)
        else:
            # Include LocationConstraint for other regions
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        
        print(f'Bucket "{bucket_name}" created successfully in {region or "us-east-1"}.')
    except ClientError as e:
        print(f'Error creating bucket: {e}')
        return False  # Indicate failure
    return True  # Indicate success

def upload_to_s3(file, username):
    s3 = get_s3_client()

    try:
        # Define the key (file path) for S3
        file_key = f"media/profile_pictures/{username}.jpg"
        
        # Upload file to S3 bucket
        s3.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, file_key)
        
        # Return the S3 URL or key
        file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{file_key}"
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
        print(f"Pre-signed URL: {response}")
        return response
    except ClientError as e:
        print(f"Error generating pre-signed URL: {e.response['Error']['Message']}")
        return None

def get_profile_picture(file_name):
    """Generate the pre-signed URL for the user's profile picture."""
    key = f"{settings.AWS_LOCATION}/{file_name}"
    #key = f"media/profile_pictures/urvashi.jpg"
    return generate_presigned_url(settings.AWS_STORAGE_BUCKET_NAME, key)

def list_profile_pictures():
    """List all profile pictures stored in S3."""
    s3_client = get_s3_client()
    try:
        response = s3_client.list_objects_v2(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Prefix=f"{settings.AWS_LOCATION}/"  # Folder prefix for profile pictures
        )
        files = [obj['Key'] for obj in response.get('Contents', [])]
        return files
    except ClientError as e:
        print(f"Error listing profile pictures: {e}")
        return []

if __name__ == "__main__":
    file_name = "urvashi.jpg"  # Replace with the actual file name
    profile_pic_url = get_profile_picture(file_name)
    print(f"Profile picture URL: {profile_pic_url}")

    profile_pictures = list_profile_pictures()
    print("Profile pictures:", profile_pictures)
