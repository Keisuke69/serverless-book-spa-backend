import boto3
import uuid
import json
import logging
import os
import datetime
import decimal
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb',region_name = 'ap-northeast-1')
table = dynamodb.Table(os.getenv('TABLE_NAME'))

def lambda_handler(event, context):
    try:
        photo_id = event['pathParameters']['id']
        
        try:
            response = table.delete_item(
                Key={
                    'photo_id': photo_id,
                }
            )
        except ClientError as e:
            logging.info(e.response['Error']['Message'])
            response = {
                'statusCode': '400',
                'body': e.response['Error']['Message'],
                'headers': {
                    'Content-Type': 'application/json',
                },
            }
            
            return response
        else:
            logging.info('Item (photo_id = ' + photo_id +') is sucessfully deleted')
            
            response = {
                'statusCode': '204',
                'body': '',
                'headers': {
                    'Content-Type': 'application/json',
                },
            }
            return response
            
    except Exception as e:
        logging.error("type : %s", type(e))
        logging.error(e)