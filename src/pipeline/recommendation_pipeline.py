import os
import sys
from src.logger import logging
from src.exception import CustomException
from src.components.recommendation_builder import BuildRecommendation

class recommendRestaurant:
    def __init__(self) -> None:
        pass

    def get_recommend(self,title):
        try:    
            logging.info("recommendation initiated..")
            obj = BuildRecommendation()
            data = obj.initiate_data_ingestion()
            model = obj.build_recommendation(data)
            restaurant_list = obj.initiate_recommendation(title,data,model)
            logging.info("recommendation completed.")
            return restaurant_list
        except Exception as e:
            logging.info("Error occured in get recommend")
            raise CustomException(e,sys)    
