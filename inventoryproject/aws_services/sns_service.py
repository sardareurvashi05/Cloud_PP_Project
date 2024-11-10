import boto3
from botocore.exceptions import ClientError

sns = boto3.client('sns')

def publish_to_sns_topic(topic_arn, message, subject):
    """Publish a message to an SNS topic."""
    try:
        response = sns.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject
        )
        print(f"Message sent to {topic_arn}. Message ID: {response['MessageId']}")
    except ClientError as e:
        print(f"Error publishing message: {e}")

def subscribe_to_sns_topic(topic_arn, protocol, endpoint):
    """Subscribe to an SNS topic."""
    try:
        response = sns.subscribe(
            TopicArn=topic_arn,
            Protocol=protocol,
            Endpoint=endpoint
        )
        print(f"Subscribed to {topic_arn} with {protocol} endpoint: {endpoint}")
        return response['SubscriptionArn']
    except ClientError as e:
        print(f"Error subscribing: {e}")
        return None

def list_subscriptions(topic_arn):
    """List all subscriptions to an SNS topic."""
    try:
        response = sns.list_subscriptions_by_topic(TopicArn=topic_arn)
        return response['Subscriptions']
    except ClientError as e:
        print(f"Error listing subscriptions: {e}")
        return []
