import boto3
from botocore.exceptions import ClientError

def create_sns_topic(topic_name):
    sns = boto3.client('sns')

    try:
        response = sns.create_topic(Name=topic_name)
        print(f"Topic {topic_name} created successfully.")
        return response['TopicArn']
    except ClientError as e:
        print(f"Error creating topic: {e}")
        return None

if __name__ == "__main__":
    create_sns_topic('my-inventory-reports-topic')
