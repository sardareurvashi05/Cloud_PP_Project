import json
import boto3

# Initialize SES and SQS clients
ses = boto3.client('ses')
sqs = boto3.client('sqs')
queue_url = 'your-sqs-queue-url'

def lambda_handler(event, context):
    # Assuming the incoming event contains email data from the app
    email_data = json.loads(event['body'])  # Example: {"to": "someone@example.com", "subject": "Test", "body": "Hello"}
   
    # Process email (add validations, logging, etc.)
   
    # Send email to SQS or SNS
    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(email_data)
    )
   
    return {
        'statusCode': 200,
        'body': json.dumps('Email request processed successfully')
    }