import boto3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import os

# Configure SQS and SES (Yahoo SMTP in your case)
SQS_QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/763605845924/InventoryReportQueue'
SMTP_SERVER = 'smtp.mail.yahoo.com'
SMTP_PORT = 465  # or 587 for TLS


def get_secret():
    SMTP_USER = 'urvashisardare@yahoo.com'
    SMTP_PASSWORD = 'Upks@0589'
    return SMTP_USER, SMTP_PASSWORD

def receive_message_from_sqs():
    # Create an SQS client
    sqs_client = boto3.client('sqs', region_name='us-east-1')  # Use your region
    
    # Receive messages from the SQS queue
    response = sqs_client.receive_message(
        QueueUrl=SQS_QUEUE_URL,
        AttributeNames=['All'],
        MaxNumberOfMessages=1,
        MessageAttributeNames=['All'],
        WaitTimeSeconds=20  # Long poll to wait for a message
    )
    
    if 'Messages' in response:
        # Get the message from the queue
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        
        # Delete the message from the queue after processing it
        sqs_client.delete_message(
            QueueUrl=SQS_QUEUE_URL,
            ReceiptHandle=receipt_handle
        )
        
        return json.loads(message['Body'])  # Assuming the body contains the email details in JSON format
    
    return None

def send_email(to_address, subject, body):
    SMTP_USER, SMTP_PASSWORD = get_secret()

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server and send the email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(SMTP_USER, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(SMTP_USER, to_address, text)
        server.quit()
        print(f"Email sent to {to_address}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def process_sqs_messages(event, context):
    # Receive and process the SQS message
    message_data = receive_message_from_sqs()
    
    if message_data:
        to_address = message_data.get('email')
        subject = message_data.get('subject')
        body = message_data.get('body')
        
        if to_address and subject and body:
            # Send the email
            send_email(to_address, subject, body)
        else:
            print("Invalid message data: Missing email, subject, or body.")
    else:
        print("No new messages in SQS.")

def lambda_handler(event, context):
    # Call process_sqs_messages from the handler
    process_sqs_messages(event, context)
    


# Run the function with mock data
if __name__ == "__main__":
    mock_event = {}  # Simulate the event that would be passed by Lambda
    mock_context = None  # Context is optional for most Lambda functions
    lambda_handler(mock_event, mock_context)
    