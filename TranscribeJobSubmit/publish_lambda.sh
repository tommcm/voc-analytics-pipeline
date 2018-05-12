#bash
rm SubmitTranscribeJobLambda.zip
cd ./lib/python2.7/site-packages/
zip -r9 ../../../SubmitTranscribeJobLambda.zip *
cd ../../../
cd ./Lambda
zip -g ../SubmitTranscribeJobLambda.zip index.py
cd ..
aws lambda update-function-code --function-name wodifynotify --zip-file fileb://SubmitTranscribeJobLambda.zip --region ap-southeast-2

# aws lambda create-function \
# --region ap-southeast-2 \
# --function-name wodifynotify \
# --zip-file fileb://lambda.zip \
# --role arn:aws:iam::447119549480:role/tommcm-wodifynotify \
# --handler helloworld.handler \
# --runtime python2.7
