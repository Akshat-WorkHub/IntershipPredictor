import os,sys
import pandas as pd

from sklearn.model_selection import train_test_split

from src import constant as const
from src.exception.exception import CustomException
from src.logger.log import logging

from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact

class DataIngestion:
    def __init__(self,ingestion_config: DataIngestionConfig):
        try:
            self.ingestion_config = ingestion_config
        except Exception as e:
            raise CustomException(e,sys)

    def export_raw_data(self,dataframe: pd.DataFrame):
        try:
            raw_data_dir = self.ingestion_config.raw_dir
            os.makedirs(raw_data_dir,exist_ok=True)

            data_filepath = self.ingestion_config.raw_filepath2

            logging.info(f"Exporting raw data to: {data_filepath}")
            dataframe.to_csv(data_filepath,index=False,header=True)
            logging.info("Raw data export successful.")

        except Exception as e:
            raise CustomException(e,sys)

    def split_train_test_data(self,df: pd.DataFrame):
        try:
            train_df, test_df = train_test_split(df,test_size=self.ingestion_config.split,random_state=42)
            logging.info("Created Train and Test Data from phishing Data's Dataframe")

            ingested_dir = self.ingestion_config.ingested_dir
            os.makedirs(ingested_dir,exist_ok=True)
            logging.info("Ingested Directory Successfully created")

            train_df.to_csv(self.ingestion_config.train_filepath,index=False,header=True)
            test_df.to_csv(self.ingestion_config.test_filepath,index=False,header=True)
            logging.info("Train and Test data saved in ingested folder's files")

        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_ingestion(self):
        try:
            data_filepath = os.path.join(os.getcwd(),const.Raw_Data_dir,const.Raw_Data_File1)
            df = pd.read_csv(data_filepath)
            self.export_raw_data(df)
            self.split_train_test_data(df)

            data_ingestion_artifact = DataIngestionArtifact(
                self.ingestion_config.train_filepath,
                self.ingestion_config.test_filepath
            )

            return data_ingestion_artifact


        except Exception as e:
            raise CustomException(e,sys)