import json
import os
import config
from utils import *
import pandas as pd

class FeaturesAPI():
    def __init__(self, user_id):
        self.s3functions = S3Functions(region=config.REGION, bucket=config.BUCKET_NAME)
        self.logger = CloudWatchLogs(region=config.REGION, logGroup = config.LOG_GROUP, logStream = config.LOG_STREAM)
        self.user_id = user_id
                
    def readingDF(self):
        datasetPath = os.path.join(config.TRAINING_URI, config.TRAINING_FILENAME)
        #cols = ["id","age","years_on_the_job","nb_previous_loans","avg_amount_loans_previous","flag_own_car","status"]
        df = self.s3functions.read_parquet(s3_path=datasetPath)
        return df
    
    def getFeaturesByID(self, df):
        df1 = (df[df['id'] == self.user_id])
        df2 = df1.sort_values(by='nb_previous_loans', ascending=False).iloc[0, :]
        return df2
    
    def run(self):
        
        try:
            self.logger.saveMessage("****** Starting Preprosessing process ******")
            
            self.logger.saveMessage("****** Reading dataframe from S3 ******")
            df = self.readingDF()
            
            self.logger.saveMessage("****** Getting Features by ID... ******")
            user_df = self.getFeaturesByID(df)
            
            self.logger.saveMessage("****** Exporting features... ******")
            result = user_df.to_json(orient="records")
                        
            return result
        
        except Exception as e:
                self.logger.saveMessage(str(e))

def lambda_handler(event, context):
    
    features = FeaturesAPI(event['user_id'])
    result = features.run()
    parsed = json.loads(result)
    return {
        'statusCode': 200,
        'body': json.dumps(parsed, indent=4) 
    }
