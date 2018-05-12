import json
import urllib
import boto3
import datetime

print('Loading function')

session = boto3.Session(profile_name='sydneysummit')

s3 = boto3.client('s3')
transcribe = boto3.client('transcribe')
       
# media_path = "https://s3.amazonaws.com/%s/%s" % (bucket,key)
media_path = "https://s3.amazonaws.com/connect-qwe-708252083442-us-east-1/connect/sydney-summit/CallRecordings/travelagent-a2cc-45e8-97ed-d63893e4cb9e_20180405T18_22_UTC.wav"

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
        "ShowSpeakerLabels": True,
        "VocabularyName": "SummitDemoWords"
    },
)
        
print ("INFO Amazon Transcribe Job " + transcribe_response['TranscriptionJob']['TranscriptionJobName'], transcribe_response['TranscriptionJob']['TranscriptionJobStatus'])
        