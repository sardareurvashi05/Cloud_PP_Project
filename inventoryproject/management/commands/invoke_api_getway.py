import requests

#API Gateway created with URL: https://17izqsdi8e.execute-api.us-east-1.amazonaws.com/prod/myresource
api_id = '17izqsdi8e'
api_url = f'https://{api_id}.execute-api.us-east-1.amazonaws.com/prod/myresource'
response = requests.get(api_url)
print(response.json())  # Should print: "Hello from Lambda!"
