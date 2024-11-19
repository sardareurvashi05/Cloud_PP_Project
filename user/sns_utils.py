import boto3
import logging

sns_client = boto3.client('sns')

def check_or_create_sns_topic(topic_name):
    # List all topics
    response = sns_client.list_topics()
    topics = response.get('Topics', [])
    
    # Search for the topic
    for topic in topics:
        if topic_name in topic['TopicArn']:
            print(f"Topic {topic_name} exists: {topic['TopicArn']}")
            return topic['TopicArn']
    
    # If not found, create the topic
    print(f"Topic {topic_name} does not exist. Creating...")
    response = sns_client.create_topic(Name=topic_name)
    return response['TopicArn']

def publish_to_sns(topic_arn, message, subject):
    try:
        # Attempt to send the message to SNS
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject
        )
        # Log the successful publish
        logging.info(f"Successfully published to SNS. Message ID: {response['MessageId']}")
        print(f"Published message to SNS topic: {topic_arn}")
    except Exception as e:
        # Log any exception that occurs
        logging.error(f"Error publishing to SNS: {e}")
        print(f"Error publishing to SNS: {e}")
        
        
def subscribe_email_to_topic(topic_arn, email):
    response = sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint=email
    )
    return response
    
def check_if_subscribed(topic_arn, email):
    # List all subscriptions for the given topic ARN
    response = sns_client.list_subscriptions_by_topic(TopicArn=topic_arn)
    
    # Check if the email is already subscribed to the topic
    for subscription in response['Subscriptions']:
        if subscription['Endpoint'] == email:
            return True
    return False