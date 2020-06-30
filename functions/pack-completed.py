import datetime as dt
import boto3
import botocore
import os
from smart_open import smart_open
import time
import logging
from dateutil.tz import gettz

from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['JOBS_TABLE'])
s3_client = boto3.client('s3')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    file = event['Records'][0]['s3']['object']['key']
    bucket_name=event['Records'][0]['s3']['bucket']['name']
    logger.info("Received "+ file)
    logger.info(event)
    id=file.split('/')[1]
    presign_params={'Bucket': bucket_name, 'Key': file}
    signed = s3_client.generate_presigned_url('get_object', Params = presign_params, ExpiresIn = 1296000)
    response = table.query(
        KeyConditionExpression=Key('id').eq(id),
        IndexName='IdIndex'
    )
    userId = response['Items'][0]['userId']
    table.update_item(
            Key={'id': id, 'userId': userId},
            UpdateExpression="set jobStatus = :val, lastUpdated = :val2, results = :val3 , expires = :val4",
            ExpressionAttributeValues={
                ':val': 'completed',
                ':val2': str(dt.datetime.now()),
                ':val3': signed,
                ':val4': int(time.time())+1296000
            }
        ) 
  
if __name__ == "__main__":
    handler('', '')
