import boto3
import zipfile
import os

def create_lambda_function():
    lambda_client = boto3.client('lambda', region_name='us-east-1')

    # Path to your lambda deployment package
    lambda_code_path = 'lambda_function.zip'

    # Ensure your lambda code is packaged in a .zip format
    with zipfile.ZipFile(lambda_code_path, 'w') as zf:
        zf.write('./inventoryproject/management/commands/lambda_function.py', arcname='lambda_function.py')

    with open(lambda_code_path, 'rb') as zip_file:
        lambda_response = lambda_client.create_function(
            FunctionName='myLambdaFunction',
            Runtime='python3.8',
            Role = 'arn:aws:iam::763605845924:role/LabRole',  # Replace with your IAM role ARN
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': zip_file.read()},
            Timeout=60
        )
    print("Lambda Function Created:", lambda_response)
    
if __name__ == "__main__":
    create_lambda_function()
