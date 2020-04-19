'''
This lambda function serves request from Amazon API Gateway to create a post by storing data into Amazon DynamoDB

'''
import json
import boto3
import os


def save_data(data):
    try:
        client = boto3.client("dynamodb")
        response = client.put_item(TableName=os.getenv("DYNAMODB_TABLE"),
                                   Item=data)
        return True 
    except Exception as e:
        print(e)
        return False


def lambda_handler(event, context):
    '''
    Data structure (payload)
    {
        "title":"",
        "description":"",
        "post":""
    }
    '''
    try:
        request_data = json.loads(event['body'])
        save_data(request_data)
        return {"statusCode": 200, "body": json.dumps("{}")}
    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": json.dumps("{}")}
