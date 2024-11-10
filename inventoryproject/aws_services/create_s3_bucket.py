import boto3
from botocore.exceptions import ClientError

def create_s3_bucket(bucket_name, region):
    s3 = boto3.client('s3', region_name=region)
    
    try:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region}
        )
        print(f'Bucket {bucket_name} created successfully.')
    except ClientError as e:
        print(f'Error creating bucket: {e}')

if __name__ == "__main__":
    create_s3_bucket('my-inventory-reports-bucket', 'us-east-1')
