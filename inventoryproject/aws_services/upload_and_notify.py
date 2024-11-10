# upload_and_notify.py
import boto3
from io import BytesIO
import pandas as pd

# AWS client setup
s3 = boto3.client('s3')
sns = boto3.client('sns')
sqs = boto3.client('sqs')

# Upload report to S3
def upload_to_s3(bucket_name, file_data, key):
    try:
        s3.upload_fileobj(file_data, bucket_name, key)
        url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': key}, ExpiresIn=3600)
        print(f"File uploaded to S3: {url}")
        return url
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
        return None

# Notify via SNS
def notify_via_sns(topic_arn, message):
    try:
        sns.publish(TopicArn=topic_arn, Message=message)
        print("SNS notification sent.")
    except Exception as e:
        print(f"Error sending SNS notification: {e}")

# Send message to SQS
def send_to_sqs(queue_url, message_body):
    try:
        sqs.send_message(QueueUrl=queue_url, MessageBody=message_body)
        print("Message sent to SQS.")
    except Exception as e:
        print(f"Error sending message to SQS: {e}")

# Main workflow
if __name__ == "__main__":
    # Settings
    bucket_name = 'your-report-bucket'
    topic_arn = 'arn:aws:sns:us-west-2:123456789012:InventoryReportTopic'  # Replace with actual ARN
    queue_url = 'https://sqs.us-west-2.amazonaws.com/123456789012/InventoryReportQueue'  # Replace with actual URL
    key = 'reports/inventory_report.xlsx'

    # Create dummy data and save to Excel format
    excel_data = BytesIO()
    df = pd.DataFrame([{"Product": "Example Product", "Stock": 10}])
    df.to_excel(excel_data, index=False)
    excel_data.seek(0)

    # Upload file to S3 and notify
    s3_url = upload_to_s3(bucket_name, excel_data, key)
    if s3_url:
        message = f"New inventory report available. Download here: {s3_url}"
        notify_via_sns(topic_arn, message)
        send_to_sqs(queue_url, message)
