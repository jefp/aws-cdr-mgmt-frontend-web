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


def next_day(last):
  return last+dt.timedelta(days=1)

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

def audit(file,id):
  item = {
      'jobId': id,
      'file': file['Key'],
      'fileStatus': file['StorageClass'],
      'createdAt': str(dt.datetime.now())
  }
  if 'glacierStatus' in file:
    item['glacierStatus']=file['glacierStatus']

  details_table.put_item(Item=item)

def restore(file,id,userId):
  fl = {}
  fl['total']=1
  fl['glacier']=0
  if (file['StorageClass'] == 'DEEP_ARCHIVE' ) or (file['StorageClass'] == 'GLACIER' ):
    response = s3_client.head_object(
      Bucket=os.environ['CDR_BUCKET'],
      Key=file['Key']
    )
    if 'Restore' in response:
      file['glacierStatus']=response['Restore']
      if response['Restore'].find('ongoing-request="false"') != -1:
        copy_source = {
          'Bucket': os.environ['CDR_BUCKET'],
          'Key': file['Key']
        }
        s3_client.copy_object(
          Bucket=os.environ['RESULT_BUCKET'],
          CopySource=copy_source,
          TaggingDirective='REPLACE',
          Tagging="Type=Temp",
          Key='private/'+id+'/'+file['Key']
        )
      else:
        item = {
         'reqId': file['Key'],
         'reqId2': id,
         'createdAt': str(dt.datetime.now()),
         'userId':  userId,
         'ttl': int(time.time())+86400
        }
        restoration_table.put_item(Item=item)
        fl['glacier']=1
    else:
      s3_client.restore_object(
        Bucket=os.environ['CDR_BUCKET'],
        Key=file['Key'],
        RestoreRequest={'Days': 7, 'GlacierJobParameters': {'Tier': os.environ['RESTAURATION_TYPE']}}
      )
      item = {
        'reqId': file['Key'],
        'reqId2': id,
        'createdAt': str(dt.datetime.now()),
        'userId':  userId,
        'ttl': int(time.time())+86400
      }
      restoration_table.put_item(Item=item)
      fl['glacier']=1
  else: 
    copy_source = {
      'Bucket': os.environ['CDR_BUCKET'],
      'Key': file['Key']
    }
    s3_client.copy_object(
      Bucket=os.environ['RESULT_BUCKET'],
      CopySource=copy_source,
      TaggingDirective='REPLACE',
      Tagging="Type=Temp",
      Key='private/'+id+'/'+file['Key']
    )
  audit(file,id)
  return fl


def recover(d,id,userId):
  fl = {}
  fl['total']=0
  fl['glacier']=0
  finished=False
  response = s3_client.list_objects_v2(
   Bucket=os.environ['CDR_BUCKET'],
   Prefix=str(d.year)+'/'+ str(d.month)+'/'+  str(d.day)+'/'
  )
  if (response['KeyCount']>0):
    files = response['Contents']
    for file in files:
      flt=restore(file,id,userId)
      fl['glacier']+=flt['glacier']
      fl['total']+=flt['total']
 
  
    finished = not response['IsTruncated']
    if not finished: 
      next_token= response['NextContinuationToken']
  
    while finished == False:
      response = s3_client.list_objects_v2( 
       Bucket=os.environ['CDR_BUCKET'],
       Prefix = str(d.year)+'/'+  str(d.month)+'/'+  str(d.day)+'/',
       ContinuationToken = next_token
      )
      files = response['Contents']
      for file in files:
        audit(file,id)
        flt=restore(file,id,userId)
        fl['glacier']+=flt['glacier']
        fl['total']+=flt['total']
      finished = not response['IsTruncated']
      if not finished: 
        next_token= response['NextContinuationToken']
  return fl

def handler(event, context):
      response = {}
      id=event['id']
      userId=event['userId']
      
      response = table.query(
       KeyConditionExpression=Key('id').eq(id) & Key('userId').eq(userId)
      )
      fr=dt.datetime.strptime(str(event['from']), '%Y-%m-%d')
      to = dt.datetime.strptime(str(event['to']), '%Y-%m-%d')
      current_glacier = 0 
      try:
        current_glacier=int(str(response['Items'][0]['totalInGlacier']))
      except:
        table.update_item(
              Key={'id': event['id'], 'userId': event['userId']},
              UpdateExpression="set totalInGlacier = :val, totalFiles = :val2",
              ExpressionAttributeValues={
                  ':val': 0,
                  ':val2': 0
              })
        print("first iteration")

      table.update_item(
            Key={'id': event['id'], 'userId': event['userId']},
            UpdateExpression="set jobStatus = :val, lastUpdated = :val2, iteration = :val3",
            ExpressionAttributeValues={
                ':val': 'processing',
                ':val2': str(dt.datetime.now()),
                ':val3': str(response['Items'][0]['from'])
            }
        )
       
       #Empezar 1 hora antes
      it=next_day(fr)
      fl={}
      fl['total']=0
      fl['glacier']=0
      try:
#        while (it <= to):
          flt=recover(it,id,userId)
          fl['glacier']+=flt['glacier']
          fl['total']+=flt['total']        

          
          
          table.update_item(
               Key={'id': event['id'], 'userId': event['userId']},
               ReturnValues="UPDATED_NEW",
               UpdateExpression="set totalInGlacier = totalInGlacier + :val",
               ExpressionAttributeValues={
                   ':val': decimal.Decimal(flt['glacier'])
               }
          )
          table.update_item(
               Key={'id': event['id'], 'userId': event['userId']},
               ReturnValues="UPDATED_NEW",
               UpdateExpression="set totalFiles = totalFiles + :val",
               ExpressionAttributeValues={
                   ':val': decimal.Decimal(flt['total'])
               }
          )

        #table.update_item(
        #      Key={'id': event['id'], 'userId': event['userId']},
        #      UpdateExpression="set totalFiles = :val",
        #      ExpressionAttributeValues={
        #          ':val': fl['total']
        #      })
          if it==to and current_glacier == 0:
              send_to_pack(id,userId)
      except Exception as e:
        table.update_item(
            Key={'id': event['id'], 'userId': event['userId']},
            UpdateExpression="set jobStatus = :val, lastUpdated = :val2, jobStatusDescription = :val3",
            ExpressionAttributeValues={
                ':val': 'error',
                ':val2':  str(dt.datetime.now()),
                ':val3':  str(e)
            })
        raise e
      response = {
           "statusCode": 200,
           "id": event['id'],
           "from": it.strftime("%Y-%m-%d"),
           "to": event['to'],
           "filter": event['filter'],
           "userId": event['userId'],
           "continue": str(event['to']!=it.strftime("%Y-%m-%d"))
      }
      return response
