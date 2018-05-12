from __future__ import print_function

import json
import boto3
import urllib2
import dateutil.parser as parser

print('Loading function2')

transcribe = boto3.client('transcribe')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    
    print("Received event: " + json.dumps(event, indent=2))
    jobName = event['guid']['jobName']
    contactId = event['guid']['contactId']
    # disconnectTime = event['guid']['disconnectTime']
    # disconnectTime = parser.parse(event['guid']['disconnectTime']).isoformat()
    disconnectTime = parser.parse(event['guid']['disconnectTime']).strftime("%Y-%m-%d %H:%M:%S")
    print('INFO Changed disconnectTime format', disconnectTime)
    bucket = event['bucket']
    recordingKey = event['key']
    
    try:
        # Generate transcriptFileName
        transcriptFileName = recordingKey.replace(".wav",".json")
        transcriptFileName = transcriptFileName.replace("CallRecordings","CallTranscripts")
        print(transcriptFileName)
        
        transcribe_response = transcribe.get_transcription_job(TranscriptionJobName=jobName)
        
        print("Downloading transcript file")
        transcriptFileUri = transcribe_response['TranscriptionJob']['Transcript']['TranscriptFileUri']
        transcriptrequest = urllib2.Request(transcriptFileUri)
        transcriptFilereponse = urllib2.urlopen(transcriptrequest)
        transcriptFile_json = json.load(transcriptFilereponse) 
        
        #Add Amazon Connect ContactID and Disconenct Time generated from file name
        transcriptFile_json.update({'ContactId': contactId})
        transcriptFile_json.update({'DisconnectTimestamp': disconnectTime})
        
        print("Uploading transcript to S3 bucket")
        s3.put_object(Body=json.dumps(transcriptFile_json), Bucket=bucket, Key=transcriptFileName)
        
        return transcriptFileName
        
    except Exception as e:
        print(e)
        message = 'Error !!!'
        print(message)
        raise Exception(message)

    return 