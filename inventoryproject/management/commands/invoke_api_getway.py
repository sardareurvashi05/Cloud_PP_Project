import boto3
import requests
from requests_aws4auth import AWS4Auth

# Set the AWS region and service
region = 'us-east-1'
service = 'execute-api'

# Get credentials from environment variables or IAM role (if running on EC2/Lambda)
session = boto3.Session()
credentials = session.get_credentials().get_frozen_credentials()

aws_auth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

url = "https://c7p0q9gyq8.execute-api.us-east-1.amazonaws.com/prod/myresource"

# Make the request using signed headers
response = requests.get(url, auth=aws_auth)

print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}")
