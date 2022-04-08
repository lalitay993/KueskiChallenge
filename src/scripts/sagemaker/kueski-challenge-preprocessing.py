import argparse
import pandas as pd
from datetime import datetime, date

class Preprosessing():
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--training_model_path', type=str)
        parser.add_argument('--dataset_path', type=str)
        args, _ = parser.parse_known_args()  
        
        self.datasetPath = args.dataset_path
        self.trainingModelPath = args.training_model_path
       
    def readingDF(self):
        df = pd.read_csv(self.datasetPath)
        df.shape
        df.head()
        return df

    def runPreprocessing(self, df):
        
        df = df.sort_values(by=["id", "loan_date"])
        df = df.reset_index(drop=True)
        df["loan_date"] = pd.to_datetime(df.loan_date)
        df.head(2)

        # Feature nb_previous_loans
        df_grouped = df.groupby("id")
        df["nb_previous_loans"] = df_grouped["loan_date"].rank(method="first") - 1

        # Feature avg_amount_loans_previous
        df['avg_amount_loans_previous'] = (
            df.groupby('id')['loan_amount'].apply(lambda x: x.shift().expanding().mean())
        )

        # Feature age
        df['birthday'] = pd.to_datetime(df['birthday'], errors='coerce')
        df['age'] = (pd.to_datetime('today').normalize() - df['birthday']).dt.days // 365

        # Feature years_on_the_job
        df['job_start_date'] = pd.to_datetime(df['job_start_date'], errors='coerce')
        df['years_on_the_job'] = (pd.to_datetime('today').normalize() - df['job_start_date']).dt.days // 365

        # Feature flag_own_car
        df['flag_own_car'] = df.flag_own_car.apply(lambda x : 0 if x == 'N' else 1)
        
        return df

    def savePreprosessingDF(self, df):
        df = df[['id', 'age', 'years_on_the_job', 'nb_previous_loans', 'avg_amount_loans_previous', 'flag_own_car', 'status']]
        df.to_parquet(self.trainingModelPath, engine='fastparquet')

    def run(self):
        try:
            df = self.readingDF()
            preprocess_df = self.runPreprocessing(df)
            self.savePreprosessingDF(preprocess_df)
        
        except Exception as e:
            print(str(e))
 
if __name__ == '__main__':
    training = Preprosessing()
    training.run()