import os 
import sys
import pandas as pd
from src.logger import logging
from dataclasses import dataclass
from src.utils import save_object
from src.exception import CustomException
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

@dataclass 
class RecommendationConfig:
    recommendation_file_path = os.path.join('artifacts','recommendation.npy')

class BuildRecommendation:
    def __init__(self):
        self.recommend_config = RecommendationConfig()

    def initiate_data_ingestion(self):
        try:
            logging.info("Data ingestion initiated")
            df=pd.read_csv(os.path.join('notebooks/data','recommend_data.csv'))
            logging.info('Dataset read as pandas Dataframe')
    
            logging.info("Data ingestion completed")
            return df
        
        except Exception as e:
            logging.info("Error occurred in data_ingestion") 
            raise CustomException(e,sys)   
    
    def build_recommendation(self,data):
        try:
            logging.info("recommendation building initiated")
            tfidf_vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = tfidf_vectorizer.fit_transform(data['cuisines'])
            cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

            save_object(
                file_path=self.recommend_config.recommendation_file_path,
                obj = cosine_sim
            )
            return cosine_sim

        except Exception as e:
            logging.info("Error occured in recommendation model building")
            raise CustomException(e,sys)    

    def initiate_recommendation(self,restaurant_name,df,cosine_sim):
        try:
            logging.info("recommendation initiated")
            idx = df[df['name'] == restaurant_name].index[0]
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:10]  
            restaurant_indices = [i[0] for i in sim_scores]

            logging.info("recommendation completed")
            return list(df['name'].iloc[restaurant_indices])

        except Exception as e:
            logging.info("Error occured in recommendation")    
            raise CustomException(e,sys)

        
