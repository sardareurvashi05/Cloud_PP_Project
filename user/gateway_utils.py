import requests
from requests_aws4auth import AWS4Auth
import boto3

def sendEmail():
    region = 'us-east-1'
    service = 'execute-api'
    session = boto3.Session()
    credentials = session.get_credentials().get_frozen_credentials()
    aws_auth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    
    url = "https://yojenau3b5.execute-api.us-east-1.amazonaws.com/prod/sendemail"
    
    try:
        response = requests.get(url, auth=aws_auth)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx/5xx)
        print(f"Response: {response.text}")
        return response.status_code
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        print(f"Response content: {err.response.content}")
    except Exception as err:
        print(f"Other error occurred: {err}")
