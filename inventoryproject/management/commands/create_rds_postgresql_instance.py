import boto3
from botocore.exceptions import ClientError


def create_rds_instance():
    # Initialize the RDS client
    rds_client = boto3.client('rds', region_name='us-east-1')  # Set your AWS region

    # Define the RDS instance parameters
    instance_params = {
        'DBName': 'InventoryManagement',                # Database name
        'DBInstanceIdentifier': 'my-rds-instance',  # Unique identifier for the instance
        'MasterUsername': 'IM',             # Master username
        'MasterUserPassword': 'IMProj12345',      # Master password
        'DBInstanceClass': 'db.t3.micro',          # Instance type
        'Engine': 'postgres',                      # Database engine
        'AllocatedStorage': 20,                    # Storage in GB
        'StorageType': 'gp2',                      # Storage type
        'BackupRetentionPeriod': 4,                # Backup retention in days
        'PubliclyAccessible': False,               # Not publicly accessible
    }

    try:
        print("Creating RDS instance...")
        response = rds_client.create_db_instance(**instance_params)
        print(response)
        print(f"RDS instance creation initiated: {response['DBInstanceIdentifier']}")

        print("Waiting for the RDS instance to be available...")
        rds_waiter = rds_client.get_waiter('db_instance_available')
        rds_waiter.wait(DBInstanceIdentifier=instance_params['DBInstanceIdentifier'])

        print(f"SUCCESS: RDS instance '{instance_params['DBInstanceIdentifier']}' is now available!")
        endpoint = get_instance_endpoint(rds_client, instance_params['DBInstanceIdentifier'])
        print(f"RDS Endpoint: {endpoint}")

    except ClientError as e:
        print(f"Failed to create RDS instance: {e}")


def get_instance_endpoint(rds_client, db_instance_identifier):
    try:
        response = rds_client.describe_db_instances(DBInstanceIdentifier=db_instance_identifier)
        return response['DBInstances'][0]['Endpoint']['Address']
    except ClientError as e:
        print(f"Failed to fetch instance endpoint: {e}")
        return None


if __name__ == "__main__":
    create_rds_instance()
