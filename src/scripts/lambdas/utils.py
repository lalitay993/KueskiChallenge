import boto3
import time
import awswrangler as wr
import pandas as pd
        
class CloudWatchLogs():
    def __init__(self, region, logGroup, logStream):
        self.client = boto3.client('logs', region_name=region)
        self.job_name = "jobName"
        self.job_run_id = "jobRunID"
        self.logGroup = logGroup
        date = time.strftime('%Y-%m-%d')
        self.logStream = f'{logStream}-{date}'
        self.initLogs()
        
    def initLogs(self):
        try:
            self.client.create_log_group(logGroupName=self.logGroup)
        except self.client.exceptions.ResourceAlreadyExistsException:
            pass

        try:
            self.client.create_log_stream(logGroupName=self.logGroup, logStreamName=self.logStream)
        except self.client.exceptions.ResourceAlreadyExistsException:
            pass
        
    def getFormatMessage(self, Msg):
        return "[{0} | {1}]: {2}".format(self.job_name, self.job_run_id, Msg)
    
    def getSeqToken(self):
        return 123
    
    def saveLogEventOnCW(self, Msg: str):
        print(Msg)
        
        response = self.client.describe_log_streams( logGroupName=self.logGroup, logStreamNamePrefix=self.logStream )
        event_log = {
        'logGroupName': self.logGroup,
        'logStreamName': self.logStream,
        'logEvents': [
            {
                'timestamp': int(round(time.time() * 1000)),
                'message': Msg
            }
        ],
        }

        if 'uploadSequenceToken' in response['logStreams'][0]:
            event_log.update({'sequenceToken': response['logStreams'][0] ['uploadSequenceToken']})

        response = self.client.put_log_events(**event_log)
        
    
    def saveMessage(self, Msg):
        Msg = self.getFormatMessage(Msg)
        self.saveLogEventOnCW(Msg)
            
class S3Functions():
    def __init__(self, region, bucket):
        self.s3_client = boto3.client('s3', region_name=region)
        self.bucket = bucket
    
    def read_parquet(self,s3_path):
        df = wr.s3.read_parquet(path=s3_path)
        return df
        
    def putObject(self, Body, URI):
        Bucket, Key = self.splitURI(URI)
        self.s3_client.put_object(Body=Body, Bucket=Bucket, Key=Key)
                
    def splitURI(self, URI):
        URI = URI.replace("s3://","")
        Key = URI[URI.find("/")+1:]
        Bucket = URI[:URI.find("/")]

        return Bucket, Key