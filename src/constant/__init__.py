import os, sys
import numpy as np

# Collection Name & DB Name used for MongoDB

Collection_Name: str = "Intership_Collection"
Database_Name: str = "IntershipDB"
PipeLine_Name: str = "Intership_Selection_Prediction"

#==========================================================
# General Variables

Target_Feature: str = "selected"
Schema_File_Path: str = os.path.join("data_schema","schema.yaml")
TrainTestSplit: float = 0.25

Expected_Model_Accuracy_Score: float = 0.6
Model_Threshold: float = 0.05 # (Used to define Overfitting or Underfitting)

Transformation_Imputer_Params: dict = {
    "missing_values" : np.nan,
    "n_neighbors" : 3,
    "weights" : "uniform"
}

#==========================================================
# File Names

Raw_Data_dir: str = "data"
Raw_Data_File1: str = "Internship_Selection_Dataset.csv"
Raw_Data_File2: str = "Final_Cleaned_Dataset.csv"

Train_Filename: str = "train.csv"
Test_Filename: str = "test.csv"
Model_Filename: str = "model.pkl"
Preprocessor_Obj: str = "preprocessor.pkl"
Drift_Report_Filename: str = "driftReport.yaml"

#==========================================================
# Directiories in Artifacts

MainDir: str = "artifact"

IngestionDir: str = "data_ingestion"
IngestionSubDir1: str = "raw_data"
IngestionSubDir2: str = "ingested_files"

ValidationDir: str = "data_validation"
ValidationSubDir1: str = "drift_report"
ValidationSubDir2: str = "valid"
ValidationSubDir3: str = "invalid"


TransformationDir: str = "data_transformation"
TransformationSubDir: str = "transformed"

ModelTrainerDir: str = "data_model_trainer"
ModelTrainerSubDir1: str = "trained_model"

SaveModelDir: str = "final_saved_models"
