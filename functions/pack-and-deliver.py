import json
import boto3
import os
import uuid
import datetime as dt
from dateutil.tz import gettz
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')

def handler(event, context):
    response = {}
    try:
       table = dynamodb.Table(os.environ['CONFIG_TABLE'])
       response = table.query(
          KeyConditionExpression=Key('Configuration').eq('AuditEnabled')
       )
       try:
         audit = str(response['Items'][0]['value'])
       except IndexError:
         audit = 0 
       table = dynamodb.Table(os.environ['AUDIT_TABLE'])
       response = table.query(
          KeyConditionExpression=Key('id').eq(event['id'])
       )

       table = dynamodb.Table(os.environ['AUDIT_TABLE'])

       table.update_item(
            Key={'id': event['id']},
            UpdateExpression="set approval_required = :val, status = :status",
            ExpressionAttributeValues={
                ':val': audit,
                ':status': 'pending_approval'
            }
        )

       response = {
           "statusCode": 200,
           "audit": audit,
           "id": event['id']
       }

    except Exception as e:
      response = {
           "statusCode": 403,
           "error": str(e)
           }
    return response
