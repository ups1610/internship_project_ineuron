import os
import sys
from src.logger import logging
from src.utils import save_object
from dataclasses import dataclass
from src.exception import CustomException
from sklearn.preprocessing import LabelEncoder



from src.components.data_ingestion import DataIngestion

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts','preprocessed_zomato.csv')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformation(self,df):
        try:
            logging.info('Data Transformation initiated')
            
            #### Encoding categrical Features: ##########
            encoder = LabelEncoder()
            df.location = encoder.fit_transform(df.location)
            df.rest_type = encoder.fit_transform(df.rest_type)
            df.cuisines = encoder.fit_transform(df.cuisines)
                    
            
            logging.info('Data Transformation completed')
            return df

        except Exception as e:
            logging.info("Error in Data Trnasformation")
            raise CustomException(e,sys)
        
    def initaite_data_transformation(self,data):
        try:
            # Reading train and test data
            df = data

            # drop unwanted columns
            logging.info("Dropping Non required features")
            unwanted_col = ['address','name','menu_item','city','dish_liked','type']
            df.drop(columns=unwanted_col,axis=1,inplace=True)

            logging.info('Obtaining preprocessing object')
            processed_df = self.get_data_transformation(df)

            logging.info('Read preprocesed data completed')
            logging.info(f'Processed Dataframe Head : \n{processed_df.head().to_string()}')
            
            target_column_name = 'rate'
            drop_columns = [target_column_name]

            input_feature_df = processed_df.drop(columns=drop_columns,axis=1)
            target_feature_df=processed_df[target_column_name]

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=processed_df
            )

            logging.info("Preprocessed file saved")

            return (
                input_feature_df,
                target_feature_df,
                self.data_transformation_config.preprocessor_obj_file_path
            )
            
        except Exception as e:
            logging.info("Exception occured in the initiate_datatransformation")

            raise CustomException(e,sys)
        
        