from __future__ import print_function

import os
import base64
import json
import boto3

print('Loading function')

comprehend = boto3.client('comprehend')
firehose = boto3.client('firehose')

# Environment Vars
sentimentStream = os.environ['SENTIMENT_STREAM']
entityStream = os.environ['ENTITY_STREAM']
phrasesStream = os.environ['PHRASES_STREAM']


def lambda_handler(event, context):
    output = []

    for record in event['records']:
        print('INFO:', record['recordId'])
        payload = base64.b64decode(record['data'])

        # Do custom processing on the payload here
        payload_json = json.loads(payload)
        # recordingLocation = payload_json['Recording']['Location']
        print (payload_json)
        
        transcript = payload_json['results']['transcripts'][0]['transcript']
        print ("INFO Transcript:", transcript)
        
        # # Detecting Language
        language_response = comprehend.detect_dominant_language(Text=transcript)
        language_code = language_response['Languages'][0]['LanguageCode']
        payload_json.update({'LanguageCode': language_code})
        print('INFO Language Code:', language_code)
        
        # Detecting Sentiment
        sentiment_response = comprehend.detect_sentiment(Text=transcript, LanguageCode=language_code)
        sentiment = sentiment_response['Sentiment']
        sentiment_score = sentiment_response['SentimentScore']
        payload_json.update({'Sentiment': sentiment})
        payload_json.update({'SentimentScore': sentiment_score})
        print('INFO Sentiment:', sentiment)
        print('INFO Sentiment Score:', sentiment_score)
        
        # # sentiment_json_data = json.dumps(json_content)
        # # print("INFO: Sending Sentiment response...")
        # # response = firehose.put_record(
        # #     DeliveryStreamName=sentimentStream,
        # #     Record={
        # #         'Data':sentiment_json_data 
        # #     }
        # # )
        
        # Detecting Entities
        entities_response = comprehend.detect_entities(Text=transcript, LanguageCode=language_code)
        entities = entities_response['Entities']
        payload_json.update({'Entities': entities})
        print('INFO Entities:', entities)
        
        # Detecing key phrases
        keyphrases_response = comprehend.detect_key_phrases(Text=transcript, LanguageCode=language_code)
        keyphrases = keyphrases_response['KeyPhrases']
        payload_json.update({'KeyPhrases': keyphrases})
        print('INFO KeyPhrases:', keyphrases)
                          
        processed_payload = json.dumps(payload_json)

        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': base64.b64encode(processed_payload)
        }
        output.append(output_record)

    print('Successfully processed {} records.'.format(len(event['records'])))

    # splitting into separate streams and enriched data by types
    create_sentiment_entities_phrases_objects(payload_json)

    return {'records': output}


def create_sentiment_entities_phrases_objects(payload_json):
    # sentiment record (ContactId, DisconnectTimestamp, transcript, sentiment, sentimentPosScore, sentimentNegScore, sentimentNeuScore, sentimentMixed)
    sentiment_object = {}
    sentiment_object['ContactId'] = payload_json['ContactId']
    sentiment_object['DisconnectTimestamp'] = payload_json['DisconnectTimestamp']
    sentiment_object['transcript'] = payload_json['results']['transcripts'][0]['transcript']
    sentiment_object['sentiment'] = payload_json['Sentiment']
    sentiment_object['sentimentPosScore'] = payload_json['SentimentScore']['Positive']
    sentiment_object['sentimentNegScore'] = payload_json['SentimentScore']['Negative']
    sentiment_object['sentimentNeuScore'] = payload_json['SentimentScore']['Neutral']
    sentiment_object['sentimentMixed'] = payload_json['SentimentScore']['Mixed']
    
    put_objects_firehose_s3(sentimentStream, json.dumps(sentiment_object))
    
    # entities record (ContactId, Disconnectimestamp, entity, type, score)
    for i in payload_json['Entities']:
        entities_object = {}
        entities_object['ContactId'] = payload_json['ContactId']
        entities_object['DisconnectTimestamp'] = payload_json['DisconnectTimestamp']
        entities_object['entity'] = i['Text']
        entities_object['type'] = i['Type']
        entities_object['score'] = i['Score']
        
        put_objects_firehose_s3(entityStream, json.dumps(entities_object))

    # keyphrases record (ContactId, DisconnectTimestamp, keyphrases)
    for i in payload_json['KeyPhrases']:
        keyphrases_object = {}
        keyphrases_object['ContactId'] = payload_json['ContactId']
        keyphrases_object['DisconnectTimestamp'] = payload_json['DisconnectTimestamp']
        keyphrases_object['phrase'] = i['Text']
        keyphrases_object['score'] = i['Score']
    
        put_objects_firehose_s3(phrasesStream, json.dumps(keyphrases_object))
    
def put_objects_firehose_s3(deliveryStreamName, data):
    response = firehose.put_record(
        DeliveryStreamName=deliveryStreamName,
        Record={
            'Data':data + '\n'
        }
    )
    print('INFO: put_objects_firehose_s3')
    print('INFO: Stream: {0} Payload: {1}'.format(deliveryStreamName,data))