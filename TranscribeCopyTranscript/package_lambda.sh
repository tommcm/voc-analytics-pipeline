#bash
rm CopyTranscriptJobLambda_1-0-0.zip
cd ./lib/python2.7/site-packages/
zip -r9 ../../../CopyTranscriptJobLambda_1-0-0.zip *
cd ../../../
cd ./Lambda
zip -g ../CopyTranscriptJobLambda_1-0-0.zip index.py
cd ..
aws s3 cp CopyTranscriptJobLambda_1-0-0.zip s3://tommcm-demo-us-east-1/voc-analytics/CopyTranscriptJobLambda_1-0-0.zip