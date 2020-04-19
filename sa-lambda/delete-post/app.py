'''
This lambda function serves request from Amazon API Gateway to delete a single post from Amazon DynamoDB

'''
import json
import boto3
import os


def delete_data(data):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.getenv("DYNAMODB_TABLE"))
    response = table.delete_item(
        Key={
            'ID': data['id']
        }
    )
    return response['Item']


def lambda_handler(event, context):
    try:
        request_data = json.loads(event['body'])
        delete_data(request_data)
        return {"statusCode": 200, "body": json.dumps("{}")}
    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": json.dumps("{}")}
