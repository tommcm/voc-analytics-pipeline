from __future__ import print_function

import json
import urllib
import boto3
import datetime

print('Loading function')

s3 = boto3.client('s3')
transcribe = boto3.client('transcribe')

def lambda_handler(event, context):
    # Get the object from the event and show its content type
    bucket = event['bucket']    
    key = event['key']
    
    try:
        
        media_path = "https://s3.amazonaws.com/%s/%s" % (bucket,key)

        # extract Call Recording UID to be used as Jobname
        # sample call recording filename '5b7a59b2-f54c-4c3e-9e07-2156df2169c1_20180315T05:57_UTC.wav'
        recordingFilename = key.split('/')[-1]
        contactId = recordingFilename.split('_')[0]
        disconnectTime = recordingFilename.split('_')[1]
        
        # jobName = 'AmazonConnectCall_' + recordingFilename.split('_')[0]
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        jobName = 'AmazonConnect_' + timestamp + '_' + recordingFilename.split('_')[0]
        
        print ('INFO Media Path: ' + media_path)
        print ('INFO Jobname: ' + jobName)
        
        transcribe_response = transcribe.start_transcription_job(
            TranscriptionJobName=jobName,
            LanguageCode='en-US',
            # SampleRate is now an optional param
            #MediaSampleRateHertz=8000, #Amazon Connect Telephony rate 
            MediaFormat='wav',
            Media={
                'MediaFileUri': media_path
            },
            Settings={ 
                "MaxSpeakerLabels": 2,
                "ShowSpeakerLabels": True
            },
        )
        
        print ("INFO Amazon Transcribe Job " + transcribe_response['TranscriptionJob']['TranscriptionJobName'], transcribe_response['TranscriptionJob']['TranscriptionJobStatus'])
        
        return {
            'jobName' : jobName,
            'contactId': contactId,
            'disconnectTime': disconnectTime
        }
        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
