import json
import boto3
import os
import uuid
import datetime as dt
from dateutil.tz import gettz

dynamodb = boto3.resource('dynamodb')

def handler(event, context):
    response = {}
    steps = boto3.client('stepfunctions')
    try:
        table = dynamodb.Table(os.environ['JOBS_TABLE'])
        for record in event.get('Records'):
            if record.get('eventName') in ('INSERT'):
                record = record['dynamodb']
                fr = record['NewImage']['from']['S']
                to = record['NewImage']['to']['S']
                filter = record['NewImage']['filter']['S']
                id = record['NewImage']['id']['S']
                userId= record['NewImage']['userId']['S']
                item = {
                    'id': id,
                    'from': fr,
                    'to': to,
                    'filter': filter,
                    'userId': userId
                    }
                response_s = steps.start_execution(
                    stateMachineArn=os.environ['STEPS_FUNC'],
                    name= id,
                    input = json.dumps(item)
                 )
                table.update_item(
                     Key={'id': id, 'userId': userId},
                     UpdateExpression="set stepFunctionARN = :val",
                     ExpressionAttributeValues={
                         ':val': response_s['executionArn']
                     }
                 )

        response = {
           "statusCode": 200
        }
    except Exception as e:
      response = {
           "statusCode": 403,
           "error": str(e)
           }
    return response
