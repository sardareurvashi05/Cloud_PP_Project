import boto3
import json

def create_secret(secret_name, secret_value, region_name='us-east-1'):
    """
    Creates a secret in AWS Secrets Manager.

    :param secret_name: Name of the secret
    :param secret_value: Dictionary containing the secret key-value pairs
    :param region_name: AWS region where the secret will be created
    """
    # Initialize the Secrets Manager client
    client = boto3.client('secretsmanager', region_name=region_name)

    try:
        # Create the secret
        response = client.create_secret(
            Name=secret_name,
            SecretString=json.dumps(secret_value)  # Convert dict to JSON string
        )
        print(f"Secret created successfully: {response['ARN']}")
        return response
    except client.exceptions.ResourceExistsException:
        print(f"Secret {secret_name} already exists.")
    except Exception as e:
        print(f"Failed to create secret: {e}")

if __name__ == "__main__":
    # Define the secret name and value
    secret_name = "my-smtp-credentials-inventory"
    secret_value = {
        "SMTP_USER": "urvashisardare@yahoo.com",
        "SMTP_PASSWORD": "Upks@0589"
    }

    # Call the function to create the secret
    create_secret(secret_name, secret_value)
