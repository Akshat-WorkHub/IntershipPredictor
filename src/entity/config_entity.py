import os
from datetime import datetime
from src import constant as const

class MainConfig:
    def __init__(self,timestamp = datetime.now()):
        self.pipeline = const.PipeLine_Name

        self.dir_name = const.MainDir
        self.time = timestamp.strftime("%d_%m_%Y_%H_%M_%S")
        self.dir = os.path.join(self.dir_name,self.time)

class DataIngestionConfig:
    def __init__(self, main_config: MainConfig):
        self.ingestion_dir = os.path.join(main_config.dir,const.IngestionDir)
        self.raw_dir = os.path.join(self.ingestion_dir,const.IngestionSubDir1)
        self.ingested_dir = os.path.join(self.ingestion_dir,const.IngestionSubDir2)

        self.raw_filepath1 = os.path.join(self.raw_dir,const.Raw_Data_File1)
        self.raw_filepath2 = os.path.join(self.raw_dir,const.Raw_Data_File2)
        self.train_filepath = os.path.join(self.ingested_dir,const.Train_Filename)
        self.test_filepath = os.path.join(self.ingested_dir,const.Test_Filename)

        self.collection = const.Collection_Name
        self.db = const.Database_Name
        self.split = const.TrainTestSplit

class DataValidationConfig:
    def __init__(self, main_config: MainConfig):
        self.validation_dir = os.path.join(main_config.dir,const.ValidationDir)
        self.drift_report_dir = os.path.join(self.validation_dir,const.ValidationSubDir1)
        self.valid_dir = os.path.join(self.validation_dir,const.ValidationSubDir2)
        self.invalid_dir = os.path.join(self.validation_dir,const.ValidationSubDir3)

        self.drift_report_filepath = os.path.join(self.drift_report_dir,const.Drift_Report_Filename)

        self.valid_train_filepath = os.path.join(self.valid_dir,const.Train_Filename)
        self.valid_test_filepath = os.path.join(self.valid_dir,const.Test_Filename)

        self.invalid_train_filepath = os.path.join(self.invalid_dir,const.Train_Filename)
        self.invalid_test_filepath = os.path.join(self.invalid_dir,const.Test_Filename)

class DataTransformationConfig:
    def __init__(self, main_config: MainConfig):
        self.transformation_dir = os.path.join(main_config.dir,const.TransformationDir)

        self.transformed_train_filepath = os.path.join(self.transformation_dir,const.Train_Filename.replace("csv","npy"))
        self.transformed_test_filepath = os.path.join(self.transformation_dir,const.Test_Filename.replace("csv","npy"))

        self.transformed_object_filepath = os.path.join(self.transformation_dir,const.Preprocessor_Obj)
        

class ModelTrainerConfig:
    def __init__(self, main_config: MainConfig):
        self.model_trainer_dir = os.path.join(main_config.dir,const.ModelTrainerDir)
        self.final_trained_model_filepath = os.path.join(self.model_trainer_dir,const.ModelTrainerSubDir1,const.Model_Filename)

        self.accuracy = const.Expected_Model_Accuracy_Score
        self.threshold = const.Model_Threshold

        


