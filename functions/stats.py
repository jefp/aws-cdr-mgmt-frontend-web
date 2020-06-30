import datetime
import boto3
import botocore
import os
import decimal
import json
import datetime as dt
from dateutil.tz import gettz
import time


dynamodb = boto3.resource('dynamodb')

def next_day(last):
  return last+dt.timedelta(days=1)

def decoder(stat):
    res = {}
    res['total_files']=str(stat['total_files'])
    res['size']=str(stat['size'])
    res['total_cdr']=str(stat['total_cdr'])
    return res

def handler(event, context):
    response = {}
    table = dynamodb.Table(os.environ['STATS_TABLE'])
        # fetch todo from the database
    fr = dt.datetime.strptime(str(event.get('queryStringParameters',{}).get('from')), '%Y-%m-%d')
    to = dt.datetime.strptime(str(event.get('queryStringParameters',{}).get('to')), '%Y-%m-%d')
    it = fr
    result={}
    while (it <= to):
        result_day = table.get_item(
            Key={'id': str(it.date()) }
        )
        if 'Item' in result_day:
            result[str(it.date())]=decoder(result_day['Item'])
        it=next_day(it)

    result_global = table.get_item(
        Key={'id': 'global' }
    )

    if 'Item' in result_global:
        result['global']=decoder(result_global['Item'])

    response = {
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true"
        },
        "statusCode": 200,
        "body": json.dumps(result)
    }
    return response