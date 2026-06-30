import os,sys
from scipy.stats import ks_2samp
import pandas as pd

from src.constant import Schema_File_Path

from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import (
    DataIngestionArtifact, 
    DataValidationArtifact
)

from src.exception.exception import CustomException
from src.logger.log import logging

from src.utils.main_utils import read_yaml_file, write_yaml_file

class DataValidation:
    def __init__(self, validation_config: DataValidationConfig, ingestion_artifact: DataIngestionArtifact):
        try:
            self.validation_config = validation_config
            self.ingestion_artifact = ingestion_artifact

            self._schema_config = read_yaml_file(Schema_File_Path)
        except Exception as e:
            raise CustomException(e,sys)
        
    def validate_no_of_columns(self, df: pd.DataFrame, dataframe_name: str) -> bool:
        try:
            no_of_cols = len(self._schema_config["columns"])
            logging.info(f"{dataframe_name} Required No. of Columns : {no_of_cols}")
            logging.info(f"{dataframe_name} has Columns : {len(df.columns)}")

            return True if len(df.columns) == no_of_cols else False
                
        except Exception as e:
            raise CustomException(e,sys)

    def detect_dataset_drift(self, base_df, current_df, threshold=0.05) -> bool:
        try:
            status = True # True means no drift detected across the dataset
            report = {}

            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                # Perform Kolmogorov-Smirnov test
                is_same_dist = ks_2samp(d1, d2)

                # Logic: If p-value < 0.05, the distributions are significantly different (Drift)
                if is_same_dist.pvalue < threshold:
                    drift_found = True
                    status = False  # If even one column drifts, overall status is False
                else:
                    drift_found = False

                report.update({column: {
                    "p_value": float(is_same_dist.pvalue),
                    "drift_status": drift_found
                }})

            drift_report_filepath = self.validation_config.drift_report_filepath
            os.makedirs(os.path.dirname(drift_report_filepath), exist_ok=True)
            write_yaml_file(drift_report_filepath, report)

            return status

        except Exception as e:
            raise CustomException(e, sys)


    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_filepath = self.ingestion_artifact.train_filepath
            test_filepath = self.ingestion_artifact.test_filepath

            train_df = pd.read_csv(train_filepath)
            test_df = pd.read_csv(test_filepath)
            
            error_msg = ""
            valid_train_status, valid_test_status = ( 
                self.validate_no_of_columns(train_df,"Train DataFrame"), 
                self.validate_no_of_columns(test_df,"Test DataFrame")
            )
            if not valid_train_status:
                error_msg += f"Train DataFrame doesn't contain all the columns in it.\n"

            if not valid_test_status:
                error_msg += f"Test DataFrame doesn't contain all the columns in it.\n"
                
            if error_msg:
                raise Exception(error_msg)
            
            drift_status = self.detect_dataset_drift(base_df=train_df, current_df=test_df)
            
            
            os.makedirs(os.path.dirname(self.validation_config.valid_train_filepath),exist_ok=True)
            train_df.to_csv(self.validation_config.valid_train_filepath,index=False,header=True)

            os.makedirs(os.path.dirname(self.validation_config.valid_test_filepath),exist_ok=True)
            test_df.to_csv(self.validation_config.valid_test_filepath,index=False,header=True)
                
                            
            data_validation_artifact = DataValidationArtifact(
                validation_status=drift_status,

                valid_train_filepath=self.validation_config.valid_train_filepath,
                invalid_train_filepath=None,

                valid_test_filepath=self.validation_config.valid_test_filepath,
                invalid_test_filepath=None,

                drift_report_filepath=self.validation_config.drift_report_filepath
            )

            return data_validation_artifact

        except Exception as e:
            raise CustomException(e,sys)