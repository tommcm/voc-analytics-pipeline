aws cloudformation create-stack \
  --stack-name voc-pipeline-`echo $(date +%s)` \
  --template-body file://voc-pipeline-master.yaml \
  --region us-east-1 \
  --disable-rollback \
    --parameters \
    "[{ \"ParameterKey\": \"AmazonConnectInstanceAliasParameter\", \"ParameterValue\": \"tommcm-summit\" }, \
      { \"ParameterKey\": \"stateMachineExecutionNamePrefixParameter\", \"ParameterValue\": \"AmazonConnect\" }, \
      { \"ParameterKey\": \"waitTimeParameter\", \"ParameterValue\": \"5\" } ]" \
        --capabilities CAPABILITY_NAMED_IAM