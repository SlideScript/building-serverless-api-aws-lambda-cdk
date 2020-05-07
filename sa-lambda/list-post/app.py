'''
This lambda function serves request from Amazon API Gateway to get all posts from Amazon DynamoDB

'''
import json
import boto3
import os


def list_data():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.getenv("DYNAMODB_TABLE"))
    response = table.scan()
    posts = []
    for item in response['Items']:
        post = {"ID": item["ID"], "title": item["title"]}
        posts.append(post)
    return posts


def lambda_handler(event, context):
    try:
        posts = list_data()
        return {"statusCode": 200, "body": json.dumps(posts)}
    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": json.dumps({})}
