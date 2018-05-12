from __future__ import print_function

import json
import boto3

print('Loading function')

transcribe = boto3.client('transcribe')

def lambda_handler(event, context):

    # Log the received event
    print("Received event: " + json.dumps(event, indent=2))
    jobName = event['jobName']
    try:
        # Query Job Status
        print("Checking job status")
        response = transcribe.get_transcription_job(TranscriptionJobName=jobName)
        # Log response from Amazon Transcribe
        print(response)
        # Return the jobStatus
        jobStatus = response['TranscriptionJob']['TranscriptionJobStatus']
        print("Job status: ", jobStatus)
        return jobStatus
        
    except Exception as e:
        print(e)
        message = 'Error getting job status!!!!'
        print(message)
        raise Exception(message)