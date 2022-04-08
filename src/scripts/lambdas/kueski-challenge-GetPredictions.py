import json
import os
import config
from utils import *
import pandas as pd
from collections.abc import Mapping

class PredictionsAPI():
    def __init__(self, event):
        self.s3functions = S3Functions(region=config.REGION, bucket=config.BUCKET_NAME)
        self.logger = CloudWatchLogs(region=config.REGION, logGroup = config.LOG_GROUP, logStream = config.LOG_STREAM)
        self.sagemaker_runtime = boto3.client('sagemaker-runtime', region_name=config.REGION)
        self.event = event
           
    def getPrediction(self):
        
        request_body = json.dumps(self.event)
        response = self.sagemaker_runtime.invoke_endpoint(EndpointName = config.ENDPOINT, ContentType = 'application/json', Body = request_body)
        predictions = json.loads(response['Body'].read())
        
        return predictions
    
    def run(self):
        
        try:
            self.logger.saveMessage("****** Starting Inference process ******")
            result = self.getPrediction()
            self.logger.saveMessage("****** Finished Inference process ******")
                        
            return result
        
        except Exception as e:
                self.logger.saveMessage(str(e))

def lambda_handler(event, context):
    
    predicts = PredictionsAPI(event)
    predictions = predicts.run()
    
    return {
        'statusCode': 200,
        'body': json.dumps({'predictions': predictions})
    }

''' 
case = {
    '5008804': [32, 12, 2, 119.45, 1],
    '5008807': [65, 0, 1, 10000, 1]
}

print(lambda_handler(case['5008807'],1)) '''
