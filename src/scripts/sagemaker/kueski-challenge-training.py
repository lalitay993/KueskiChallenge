import pandas as pd
import matplotlib.pyplot as plt
#%matplotlib inline

from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, confusion_matrix, recall_score, 
    plot_confusion_matrix, precision_score, plot_roc_curve
)
from sklearn.ensemble import RandomForestClassifier
from joblib import dump

import os
import argparse
import tempfile

class Training():
    def __init__(self): 
        parser = argparse.ArgumentParser()
        parser.add_argument('--training_model_path', type=str)
        parser.add_argument('--model_path', type=str)
        args, _ = parser.parse_known_args()  
        
        self.modelPath = args.model_path
        self.trainingModelPath = args.training_model_path
        #self.trainingModelPath = 's3://kueski-challenge-dev/preprocessing/train_model.parquet'
        #self.modelPath = "algo"

    def readingDF(self):
        cols = ["id","age","years_on_the_job","nb_previous_loans","avg_amount_loans_previous","flag_own_car","status"]
        df = pd.read_parquet(self.trainingModelPath, columns=cols)
        
        df.head()
        df.dtypes
        df.status.hist()
        cust_df = df.copy()
        cust_df.fillna(0, inplace=True)
        
        return cust_df
        
    def trainingModel(self, cust_df):
        Y = cust_df['status'].astype('int')

        cust_df.drop(['status'], axis=1, inplace=True)
        cust_df.drop(['id'], axis=1, inplace=True)
        
        X = cust_df
        
        X_train, X_test, y_train, y_test = train_test_split(X, Y, stratify=Y, test_size=0.3, random_state = 123)
        
        # Using Synthetic Minority Over-Sampling Technique(SMOTE) to overcome sample imbalance problem.
        #Y = Y.astype('int')
        X_train, y_train = SMOTE().fit_resample(X_train, y_train)
        X_train = pd.DataFrame(X_train, columns=X.columns)
        
        model = RandomForestClassifier(n_estimators=5)

        model.fit(X_train, y_train)
        y_predict = model.predict(X_test)

        print('Accuracy Score is {:.5}'.format(accuracy_score(y_test, y_predict)))
        print('Precision Score is {:.5}'.format(precision_score(y_test, y_predict)))
        print('Recall Score is {:.5}'.format(precision_score(y_test, y_predict)))
        print(pd.DataFrame(confusion_matrix(y_test,y_predict)))
        
        return model
        
    def modelPersistence(self, model):
        dump(model, self.modelPath) 
            
    def run(self):
        try:
            cust_df = self.readingDF()
            model = self.trainingModel(cust_df)
            self.modelPersistence(model)
        
        except Exception as e:
            print(str(e))
            
if __name__ == '__main__':
    training = Training()
    training.run()