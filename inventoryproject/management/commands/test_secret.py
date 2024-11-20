import boto3
import json

def get_encrypted_secret(secret_name, region_name='us-east-1'):
    client = boto3.client('secretsmanager', region_name=region_name)

    try:
        response = client.get_secret_value(SecretId=secret_name)
        
        # The decrypted secret is returned as a JSON string
        secret_value = json.loads(response['SecretString'])
        return secret_value
    except Exception as e:
        print(f"Failed to retrieve secret: {e}")
        return None

if __name__ == "__main__":
    secret_name = "my-smtp-credentials-inventory"
    secret = get_encrypted_secret(secret_name)
    if secret:
        print("Decrypted secret:", secret)
