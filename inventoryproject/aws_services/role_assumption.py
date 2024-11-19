import boto3

def assume_role():
    """
    Assume an IAM role with the specified ARN and return the S3 client using temporary credentials.
    """
    sts_client = boto3.client('sts')

    assumed_role = sts_client.assume_role(
        RoleArn="arn:aws:iam::763605845924:role/LabRole",  # Replace with your IAM role ARN
        RoleSessionName="SessionName"
    )

    credentials = assumed_role['Credentials']

    s3 = boto3.client(
        's3',
        aws_access_key_id=credentials[''],
        aws_secret_access_key=credentials[''],
        aws_session_token=credentials['']
    )

    return s3

# Call the function to assume the role and access S3
s3_client = assume_role()
