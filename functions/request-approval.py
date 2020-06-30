import json
import boto3
import os
import uuid
import datetime as dt
from dateutil.tz import gettz
import time

from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')

def handler(event, context):
    response = {}
    try:
       table = dynamodb.Table(os.environ['JOBS_TABLE'])
       table.update_item(
            Key={'id': event['id'], 'userId': event['userId']},
            UpdateExpression="set ApprovalCode = :val, ApprovalExpireAt = :val2",
            ExpressionAttributeValues={
                ':val': str(uuid.uuid4()),
                ':val2':  int(time.time()) + 86400*3
            }
        )

       response = {
           "statusCode": 200,
           "id": event['id']
       }

    except Exception as e:
      response = {
           "statusCode": 403,
           "error": str(e)
           }
    return response
