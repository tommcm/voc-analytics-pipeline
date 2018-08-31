#bash
rm AmazonConnectCallTranscription_1-0-0.zip
cd ./env/lib/python2.7/site-packages/
zip -r9 ../../../AmazonConnectCallTranscription_1-0-0.zip *
cd ../../../../
cd ./Lambda
zip -g ../AmazonConnectCallTranscription_1-0-0.zip index.py
cd ..
aws s3 cp AmazonConnectCallTranscription_1-0-0.zip s3://tommcm-demo-us-east-1/voc-analytics/AmazonConnectCallTranscription_1-0-0.zip --acl public-read