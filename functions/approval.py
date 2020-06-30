import json
import boto3
import os
import uuid
import datetime as dt
from dateutil.tz import gettz
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')

def next_day(last):
  return last+dt.timedelta(days=1)

def before_day(last):
  return last-dt.timedelta(days=1)

def handler(event, context):
    response = {}
    table = dynamodb.Table(os.environ['CONFIG_TABLE'])
    response = table.query(
       KeyConditionExpression=Key('Configuration').eq('AuditEnabled')
    )
    audit = "0"
    try:
      audit = str(response['Items'][0]['value'])
    except IndexError:
      audit = "10" 

    table = dynamodb.Table(os.environ['JOBS_TABLE'])
    table.update_item(
         Key={'id': event['id'], 'userId': event['userId']},
         UpdateExpression='set approvalRequired = :val, jobStatus = :st',
         ExpressionAttributeValues={
             ':val': audit,
             ':st': "pendingApproval"
         }
     )

    fr=before_day(dt.datetime.strptime(str(event['from']), '%Y-%m-%d'))
    to=next_day(dt.datetime.strptime(str(event['to']), '%Y-%m-%d'))


    response = {
        "statusCode": 200,
        "audit": audit,
        "id": event['id'],
        "userId": event['userId'],
        "from": fr.strftime("%Y-%m-%d"),
        "to": to.strftime("%Y-%m-%d"),
        "filter": event['filter'],
        "continue": 'True'
    }
    return response
