'''
This lambda function serves request from Amazon API Gateway to get a single post from Amazon DynamoDB

'''
import json
import boto3
import os


def get_data(post_ID):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.getenv("DYNAMODB_TABLE"))
    response = table.get_item(Key={'ID': post_ID})
    if "Item" in response:
        if response['Item']:
            return response['Item']
    else:
        return {}


def lambda_handler(event, context):
    try:
        post_ID = event['pathParameters']['id']
        post = get_data(post_ID)
        if post:
            return {"statusCode": 200, "body": json.dumps(post)}
        else:
            return {"statusCode": 404, "body": json.dumps(post)}
    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": json.dumps({})}
