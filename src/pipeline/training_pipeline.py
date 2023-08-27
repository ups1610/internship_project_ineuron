from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

if __name__ == "__main__":
    ingestion_obj = DataIngestion()
    data = ingestion_obj.initiate_data_ingestion()
    transform_obj = DataTransformation()
    input_feature,target_feature,_ = transform_obj.initaite_data_transformation(data)
    trainer_obj = ModelTrainer()
    trainer_obj.initate_model_training(input_feature , target_feature)
