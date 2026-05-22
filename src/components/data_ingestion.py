import os,sys
import numpy as np
import pandas as pd

from pymongo.mongo_client import MongoClient
import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

from typing import List
from sklearn.model_selection import train_test_split

from src.exception.exception import CustomException
from src.logger.log import logging

from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact

class DataIngestion:
    def __init__(self,ingestion_config: DataIngestionConfig):
        try:
            self.ingestion_config = ingestion_config
        except Exception as e:
            try:
                raise CustomException(e,sys)
            except CustomException as ce:
                print(ce)

    def export_from_mongodb_collection_as_df(self):
        '''
            Takes Data from Raw Data Filepath and convert it into DataFrame and return DataFrame.
        '''
        try:
            df = pd.read_csv('Internship_Selection_Dataset.csv')

            return df
        except Exception as e:
            try:
                raise CustomException(e,sys)
            except CustomException as ce:
                print(ce)

    def export_data_into_feature_store(self,dataframe: pd.DataFrame):
        try:
            features_store_dir = self.ingestion_config.feature_store_dir
            os.makedirs(features_store_dir,exist_ok=True)

            data_filepath = self.ingestion_config.data_filepath
            dataframe.to_csv(data_filepath,index=False,header=True)

            return dataframe
        except Exception as e:
            try:
                raise CustomException(e,sys)
            except CustomException as ce:
                print(ce)

    def split_train_test_data(self,df: pd.DataFrame):
        try:
            train_df, test_df = train_test_split(df,test_size=self.ingestion_config.split,random_state=42)
            logging.info("Created Train and Test Data from phishing Data's Dataframe")

            # ingested_dir = os.path.dirname(self.ingestion_config.train_filepath)
            ingested_dir = self.ingestion_config.ingested_dir
            os.makedirs(ingested_dir,exist_ok=True)
            logging.info("Ingested Directory Successfully created")

            train_df.to_csv(self.ingestion_config.train_filepath,index=False,header=True)
            test_df.to_csv(self.ingestion_config.test_filepath,index=False,header=True)
            logging.info("Train and Test data saved in ingested folder's files")


        except Exception as e:
            try:
                raise CustomException(e,sys)
            except CustomException as ce:
                print(ce)


    def initiate_data_ingestion(self):
        try:
            df = self.export_from_mongodb_collection_as_df()
            dataframe = self.export_data_into_feature_store(df)
            self.split_train_test_data(dataframe)

            data_ingestion_artifact = DataIngestionArtifact(self.ingestion_config.train_filepath,self.ingestion_config.test_filepath)

            return data_ingestion_artifact


        except Exception as e:
            try:
                raise CustomException(e,sys)
            except CustomException as ce:
                print(ce)