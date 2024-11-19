# report_service/report_service.py

import boto3
from botocore.exceptions import NoCredentialsError
import pandas as pd
from io import BytesIO

# Initialize AWS services
s3 = boto3.client('s3')
ses = boto3.client('ses', region_name='your-region')  # Specify your region

def upload_to_s3(file_data, bucket, key):
    try:
        s3.upload_fileobj(file_data, bucket, key)
        url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': key}, ExpiresIn=3600)
        return url
    except NoCredentialsError:
        print("Credentials not available.")
        return None

def send_email(recipient, subject, body_text, s3_url):
    ses.send_email(
        Source="your-email@example.com",
        Destination={'ToAddresses': [recipient]},
        Message={
            'Subject': {'Data': subject},
            'Body': {
                'Text': {'Data': f"{body_text}\n\nDownload your report: {s3_url}"}
            }
        }
    )

# Generate and upload the Excel report
excel_data = BytesIO()
df = pd.DataFrame([{"Product": "Example", "Stock": 10}])  # Replace with actual data
df.to_excel(excel_data, index=False)
excel_data.seek(0)

bucket_name = 'your-bucket-name'
key = 'reports/inventory_report.xlsx'
s3_url = upload_to_s3(excel_data, bucket_name, key)

# Send email with link if upload succeeded
if s3_url:
    send_email(
        recipient='recipient@example.com',
        subject='Your Inventory Report',
        body_text='Please find your inventory report below.',
        s3_url=s3_url
    )
