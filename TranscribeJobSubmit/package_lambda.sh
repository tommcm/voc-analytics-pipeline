#bash
rm SubmitTranscribeJobLambda.zip
cd ./env/lib/python2.7/site-packages/
zip -r9 ../../../SubmitTranscribeJobLambda.zip *
cd ../../../../
cd ./Lambda
pwd
zip -g ../SubmitTranscribeJobLambda.zip index.py
cd ..
pwd
aws s3 cp SubmitTranscribeJobLambda.zip s3://tommcm-demo-us-east-1/voc-analytics/SubmitTranscribeJobLambda_1-0-0.zip --acl public-read

# aws lambda create-function \
# --region ap-southeast-2 \
# --function-name wodifynotify \
# --zip-file fileb://lambda.zip \
# --role arn:aws:iam::447119549480:role/tommcm-wodifynotify \
# --handler helloworld.handler \
# --runtime python2.7

