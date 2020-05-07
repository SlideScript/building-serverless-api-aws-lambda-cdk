'''
This lambda function serves request from Amazon API Gateway to delete a single post from Amazon DynamoDB

'''
import json
import boto3
import os


def delete_data(post_ID):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.getenv("DYNAMODB_TABLE"))
    response = table.delete_item(Key={'ID': post_ID})
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False


def lambda_handler(event, context):
    try:
        post_ID = event['pathParameters']['id']
        response = delete_data(post_ID)
        if response == 200:
            return {"statusCode": 200, "body": json.dumps({})}
        else:
            return {"statusCode": 404, "body": json.dumps({})}
    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": json.dumps({})}
