'''
This lambda function serves request from Amazon API Gateway to get a single post from Amazon DynamoDB

'''
import json
import boto3
import os


def get_data(data):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.getenv("DYNAMODB_TABLE"))
    response = table.get_item(
        Key={
            'ID': data['id']
        }
    )
    return response['Item']


def lambda_handler(event, context):
    try:
        request_data = json.loads(event['body'])
        post = get_data(request_data)
        return {"statusCode": 200, "body": json.dumps(post)}
    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": json.dumps("{}")}
