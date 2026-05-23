import sys
from src.entity.artifact_entity import (
    DataIngestionArtifact,
    DataTransformationArtifact,
    DataValidationArtifact,
    ModelTrainerArtifact
)
from src.entity.config_entity import (
    MainConfig,
    DataIngestionConfig,
    DataTransformationConfig,
    DataValidationConfig,
    ModelTrainerConfig
)

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import Model_Trainer

from src.logger.log import logging
from src.exception.exception import CustomException

def main():
    try:
        main_config = MainConfig()

        logging.info("Data Ingestion has Started")
        ingestion_config = DataIngestionConfig(main_config)
        data_ingestion_obj = DataIngestion(ingestion_config)
        ingestion_artifact = data_ingestion_obj.initiate_data_ingestion()
        print(ingestion_artifact)
        print("\n\nData Ingestion Completed\n\n")
        logging.info("Data Ingestion Completed")

        logging.info("Data Validation has Started")
        validation_config = DataValidationConfig(main_config)
        data_validation_obj = DataValidation(validation_config, ingestion_artifact)
        validation_artifact = data_validation_obj.initiate_data_validation()
        print(validation_artifact)
        print("\n\nData Validation Completed\n\n")
        logging.info("Data Validation Completed")

        logging.info("Data Transformation has Started")
        transformation_config = DataTransformationConfig(main_config)
        data_transformation_obj = DataTransformation(transformation_config, validation_artifact)
        transformation_artifact = data_transformation_obj.initiate_data_transformation()
        print(transformation_artifact)
        print("\n\nData Transformation Completed\n\n")
        logging.info("Data Transformation Completed")

        logging.info("Model Training Started ")
        model_trainer_config = ModelTrainerConfig(main_config)
        model_trainer = Model_Trainer(model_trainer_config,transformation_artifact)

        model_trainer_artifact = model_trainer.initiate_model_training()
        print(model_trainer_artifact)
        print("\n\nModel Training Completed\n\n")
        logging.info("Model Training Artifact Created")

    except Exception as e:
        raise CustomException(e,sys)
if __name__ == "__main__":
    main()