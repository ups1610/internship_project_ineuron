import os
import sys
import zipfile
import pickle
import sqlite3
from src.exception import CustomException
from src.logger import logging

def com_save_object(file_path, obj,compressed_path):
    try:
        dir_path = os.path.dirname(file_path)
        com_dir_path = os.path.dirname(compressed_path)

        os.makedirs(dir_path, exist_ok=True)
        os.makedirs(com_dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

        with zipfile.ZipFile(compressed_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(file_path)

        os.remove(file_path)        

    except Exception as e:
        raise CustomException(e, sys)
    
def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)       

    except Exception as e:
        raise CustomException(e, sys)    


def load_object(file_path):
    try:
        with zipfile.ZipFile(file_path, "r") as zipf:
            zipf.extractall("extracted_data")
        with open("extracted_data/artifacts/model.pkl", "rb") as pkl_file:
            return pickle.load(pkl_file)   
            
        # with open(file_path,'rb') as file_obj:
        #     return pickle.load(file_obj)
    except Exception as e:
        logging.info('Exception Occured in load_object function utils')
        raise CustomException(e,sys)
    
def sqli_connect(db_name):
    try:
        conn = sqlite3.connect(db_name+'.db')
        logging.info("Connected to database successfully")
        return conn
    except Exception as e:
        raise CustomException(e,sys)      