import json

def lambda_handler(event, context):
    for record in event['Records']:
        message = record['body']
        print(f"Processing SQS message: {message}")
        # Add your business logic here (e.g., update inventory in the database)
    return {
        'statusCode': 200,
        'body': json.dumps('Successfully processed messages')
    }
