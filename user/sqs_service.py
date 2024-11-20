import boto3
from django.conf import settings

def send_message_to_sqs(message_body):
    # Initialize SQS client
    sqs = boto3.client(
        'sqs',
        region_name="us-east-1",
    )

    response = sqs.send_message(
        QueueUrl=settings.AWS_SQS_QUEUE_URL,
        MessageBody=message_body,
    )
    return response
