#bash
rm CheckTranscribeJobLambda_1-0-0.zip
cd ./lib/python2.7/site-packages/
zip -r9 ../../../CheckTranscribeJobLambda_1-0-0.zip *
cd ../../../
cd ./Lambda
zip -g ../CheckTranscribeJobLambda_1-0-0.zip index.py
cd ..

