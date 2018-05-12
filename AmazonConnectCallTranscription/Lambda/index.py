from __future__ import print_function

import json
import os
import urllib
import boto3
import datetime

print('Loading function')

stepfunctions = boto3.client('stepfunctions')

def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    # key = event['Records'][0]['s3']['object']['key']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    stateMachineArn = os.environ['stateMachineArn']
    stateMachineExecutionNamePrefix = os.environ['stateMachineExecutionNamePrefix']
    waittime = os.environ['waittime']
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    
    recordingFilename = key.split('/')[-1]
    
    sf_input = {}
    sf_input['waittime'] = waittime
    sf_input['bucket'] = bucket
    sf_input['key'] = key
    
    try:
        response = stepfunctions.start_execution(
        stateMachineArn=stateMachineArn,
        name=stateMachineExecutionNamePrefix + '_' + timestamp + '_' + recordingFilename.split('_')[0],
        input= json.dumps(sf_input)
    )
        return
        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e