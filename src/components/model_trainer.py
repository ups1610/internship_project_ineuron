# Basic Import
import os
import sys
import numpy as np
import pandas as pd
from src.logger import logging
from dataclasses import dataclass
from src.utils import save_object
from src.exception import CustomException
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score,f1_score,r2_score

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation

################# Model Building / Optimization ##################
@dataclass 
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts','model.pkl')


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initate_model_training(self,input_feature_df,target_feature_df):
        try:
            logging.info('Train Test Split data')
            X_train, X_test, y_train, y_test = train_test_split(
                input_feature_df,
                target_feature_df,
                test_size=0.3,
                random_state=10
            )
            
            models = {
                'LinearRegression' : LinearRegression(),
                'DecisionTree' : DecisionTreeRegressor(min_samples_leaf=0.01),
                'RandomForest' : RandomForestRegressor(n_estimators=650,random_state=245,min_samples_leaf=.0001),
                'SVR' : SVR(kernel ='rbf'),
                'ExtraTree' : ExtraTreesRegressor(n_estimators=120)
            }
            
            model_details = {}
            score = 0
            for model_name,model_instance in models.items():
                model = model_instance
                model.fit(X_train,y_train)

                # predict on test data
                y_pred = model.predict(X_test)
                acc_score = r2_score(y_test, y_pred)
                if acc_score > score :
                    score = acc_score
                    best_fit_model = model
                model_details[model_name] = [model,acc_score]
            
            logging.info("Models Details : ")
            logging.info(f"{model_details}")
            logging.info("Confusion Matrix on Test Data")
            logging.info(f"{pd.crosstab(y_test, y_pred, rownames=['True'], colnames=['Predicted'], margins=True)}")
            save_object(
                 file_path=self.model_trainer_config.trained_model_file_path,
                 obj=best_fit_model
            )
            return best_fit_model

        except Exception as e:
            logging.info('Exception occured at Model Training')
            raise CustomException(e,sys)

             