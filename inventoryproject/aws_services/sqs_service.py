import boto3
from botocore.exceptions import ClientError

sqs = boto3.client('sqs')

def send_message_to_queue(queue_url, message_body):
    """Send a message to an SQS queue."""
    try:
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body
        )
        print(f"Message sent to queue: {queue_url}. Message ID: {response['MessageId']}")
    except ClientError as e:
        print(f"Error sending message: {e}")

def receive_message_from_queue(queue_url):
    """Receive a message from an SQS queue."""
    try:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10
        )
        messages = response.get('Messages', [])
        if messages:
            return messages[0]
        else:
            print("No messages in queue.")
            return None
    except ClientError as e:
        print(f"Error receiving message: {e}")
        return None

def delete_message_from_queue(queue_url, receipt_handle):
    """Delete a message from an SQS queue."""
    try:
        response = sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        print(f"Message deleted from queue: {queue_url}")
    except ClientError as e:
        print(f"Error deleting message: {e}")
