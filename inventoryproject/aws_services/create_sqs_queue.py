# create_sqs_queue.py
import boto3

def create_sqs_queue(queue_name):
    sqs = boto3.client('sqs')
    try:
        response = sqs.create_queue(QueueName=queue_name)
        queue_url = response['QueueUrl']
        print(f"SQS Queue '{queue_name}' created with URL: {queue_url}")
        return queue_url
    except Exception as e:
        print(f"Error creating SQS queue: {e}")
        return None

# Usage
if __name__ == "__main__":
    create_sqs_queue('InventoryReportQueue')
