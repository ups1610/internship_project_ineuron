import os
import sys
import numpy as np
import pandas as pd
from src.utils import load_object
from src.logger import logging
from src.exception import CustomException

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self,features):
        try:
            logging.info("Predicting..")
            model_path=os.path.join('artifacts','compressed_model.zip')
            model=load_object(model_path)
            
            test_data = pd.DataFrame(features)
            predict_rate = model.predict(test_data)
            logging.info("Prediction done")
            return predict_rate[0]
        
        except Exception as e:
            logging.info("Error ocurred in prediction pipeline")
            raise CustomException(e,sys)    