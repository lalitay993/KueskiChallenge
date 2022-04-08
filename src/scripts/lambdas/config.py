import os

PROJECT_NAME = os.getenv("PROJECT_NAME", default = "kueski-challenge")
ENVIRONMENT = os.getenv("ENVIRONMENT", default = "dev")
REGION = os.getenv("REGION", default = "us-east-1")
BUCKET_NAME = os.getenv("BUCKET_NAME", default = f"kueski-challenge-{ENVIRONMENT}")
LOG_GROUP = os.getenv("LOG_GROUP", default = f"{PROJECT_NAME}-{ENVIRONMENT}")
LOG_STREAM = os.getenv("LOG_STREAM", default = "Sagamaker")

PREPROCESSING_INPUT = os.getenv("PREPROCESSING_INPUT", default = "/opt/ml/processing/input")
PREPROCESSING_OUTPUT = os.getenv("PREPROCESSING_OUTPUT", default = "/opt/ml/processing/output")
DATASET_FILENAME = os.getenv("DATASET_FILENAME", default = "dataset_credit_risk.csv")
DATASET_URI = os.getenv("DATASET_URI", default = f"s3://{BUCKET_NAME}/landing/")
TRAINING_FILENAME = os.getenv("TRAINING_FILENAME", default = "train_model.parquet")
TRAINING_URI = os.getenv("TRAINING_URI", default = f"s3://{BUCKET_NAME}/preprocessing/")
MODEL_FILENAME = os.getenv("MODEL_FILENAME", default = "model_risk.joblib")
MODEL_URI = os.getenv("MODEL_URI", default = f"s3://{BUCKET_NAME}/train_models/")

ENDPOINT = os.getenv("ENDPOINT", default = "KueskiEndpointModel")