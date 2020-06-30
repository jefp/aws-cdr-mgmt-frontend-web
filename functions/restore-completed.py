import json
import boto3
import os
import uuid
import datetime as dt
from dateutil.tz import gettz
import time
import decimal

from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['JOBS_TABLE'])
details_table = dynamodb.Table(os.environ['JOBS_DETAILS_TABLE'])
restoration_table = dynamodb.Table(os.environ['RESTORATION_TABLE'])
s3_client = boto3.client('s3')


def send_to_pack(id,userId):
      sqs_client = boto3.client('sqs')
      sqs_payload = json.dumps({
             "id": id
       })
      sqs_client.send_message(QueueUrl=os.environ['SQS_PACK_URL'], MessageBody=sqs_payload)
      table = dynamodb.Table(os.environ['JOBS_TABLE'])
      table.update_item(
            Key={'id': id, 'userId': userId},
            UpdateExpression="set jobStatus = :val, lastUpdated = :val2",
            ExpressionAttributeValues={
                ':val': 'sendingToPack',
                ':val2':  str(dt.datetime.now())
            }
        )

def handler(event, context):
    print(event)
    for record in event['Records']:
        print(record)
        key = json.loads(record['Sns']['Message'])['Records'][0]['s3']['object']['key']
        bucket = json.loads(record['Sns']['Message'])['Records'][0]['s3']['bucket']['name']
        response = restoration_table.query(
          KeyConditionExpression=Key('reqId').eq(key) 
         )
        print(response)
        for item in response['Items']:
            print(item)
            id = item['reqId2']
            userId = item['userId']
            values = table.update_item(
               Key={'id': id, 'userId': userId},
               ReturnValues="UPDATED_NEW",
               UpdateExpression="set totalInGlacier = totalInGlacier - :val",
               ExpressionAttributeValues={
                   ':val': decimal.Decimal(1)
               }
            )
            totalInGlacier=values['Attributes']['totalInGlacier']
            copy_source = {
                'Bucket': bucket,
                'Key': key
            }
            s3_client.copy_object(
                Bucket=os.environ['RESULT_BUCKET'],
                CopySource=copy_source,
                TaggingDirective='REPLACE',
                Tagging="Type=Temp",
                Key='private/'+id+'/'+key
            )
            details_table.update_item(
                Key={'jobId': id, 'file': key},
                UpdateExpression="set jobStatus = :val, lastUpdated = :val2",
                ExpressionAttributeValues={
                ':val': 'restored',
                ':val2': str(dt.datetime.now())
               }
            )
            if totalInGlacier ==0:
                send_to_pack(id,userId)
    return True