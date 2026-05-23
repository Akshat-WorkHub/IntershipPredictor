import os,sys
import numpy as np
import pandas as pd

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from src.constant import Target_Feature, Transformation_Imputer_Params
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import (
    DataValidationArtifact, 
    DataTransformationArtifact
)


from src.utils.main_utils import store_numpy_array, save_object

from src.exception.exception import CustomException
from src.logger.log import logging

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class FeatureGenerator(BaseEstimator, TransformerMixin):
    def __init__(self):
        # The exact order from your raw CSV
        self.raw_columns = [
            'student_id', 'CGPA', 'skills_score', 'projects_count', 
            'internships_done', 'communication_score', 'aptitude_score', 
            'coding_test_score', 'resume_score', 'extracurricular', 
            'college_tier', 'hackathons_participated', 'certifications_count', 
            'linkedin_activity_score', 'github_score', 'soft_skills_score', 
            'interview_score', 'consistency_score', 'backlogs', 
            'placement_training'
        ]

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        try:
            df = pd.DataFrame(X, columns=self.raw_columns)

            # 1. Pre-conversion: Handle categorical text before math
            # Mapping strings to numbers so math doesn't crash
            df['college_tier'] = df['college_tier'].map({'Tier 1': 3, 'Tier 2': 2, 'Tier 3': 1}).fillna(0)
            df['extracurricular'] = df['extracurricular'].map({'Yes': 1, 'No': 0}).fillna(0)
            df['placement_training'] = df['placement_training'].map({'Yes': 1, 'No': 0}).fillna(0)

            # 2. Manufacturing Logic (Your Notebook Math)
            df['technical_score'] = df[['aptitude_score', 'skills_score', 'coding_test_score', 'github_score']].mean(axis=1)
            df['candidate_score'] = df[['communication_score','extracurricular', 'resume_score', 'linkedin_activity_score', 'soft_skills_score', 'interview_score']].mean(axis=1)
            df['experience_total'] = df['internships_done'] + df['projects_count'] + df['certifications_count'] + df['hackathons_participated']
            df['academic_reliability'] = df['CGPA'] + df['consistency_score'] - (df['backlogs'] * 1) + (df['college_tier'] * 0.25 + df['placement_training'] * 0.25)
            
            df['max_tech_skill'] = df[['aptitude_score', 'skills_score', 'coding_test_score', 'github_score']].max(axis=1)
            df['max_soft_skill'] = df[['communication_score', 'interview_score', 'soft_skills_score']].max(axis=1)
            
            df['tech_candidate_multiplier'] = df['technical_score'] * df['candidate_score']
            df['no_experience_flag'] = (df['experience_total'] == 0).astype(int)
            df['high_risk_flag'] = (df['backlogs'] > 1).astype(int)

            # 3. Dropping useless/original columns
            # We drop EVERYTHING except the 10 engineered features and the target
            cols_to_keep = [
                'technical_score', 'candidate_score', 'experience_total', 
                'academic_reliability', 'max_tech_skill', 'max_soft_skill', 
                'tech_candidate_multiplier', 'no_experience_flag', 
                'high_risk_flag'
            ]
            
            return df[cols_to_keep].values
            
        except Exception as e:
            raise CustomException(e, sys)



class DataTransformation:
    def __init__(self, transformation_config: DataTransformationConfig, validation_artifact: DataValidationArtifact):
        try:
            self.data_validation_artifact: DataValidationArtifact = validation_artifact
            self.data_transformation_config: DataTransformationConfig = transformation_config
        except Exception as e:
            raise CustomException(e,sys)
        
    
    
    def get_data_transformer_object(self) -> Pipeline:
        """
            It initialises the KNN Imputer Object with the parameters specified in the training_pipeline.py file
            and returns a Scikit Learn's Pipeline Object with the KNN Imputer Object as first step.

            Input self: DataTransformation
            Ouput Return a Pipeline Object "Pipeline(["imputer",KNNImputer(**Transformation_Imputer_Params)])"
        """
        logging.info("Entered into get_data_transformer_object method of Transformation class")

        try:
            feature_generator = FeatureGenerator() # Custom Transformer responsible to convert/map orginal features into engineered features

            imputer:KNNImputer = KNNImputer(**Transformation_Imputer_Params)
            logging.info(f"Initialised KNN Imputer as a Data Transformer Object with params {Transformation_Imputer_Params}")

            processor: Pipeline = Pipeline(
                steps=[
                    ("feature_generator",feature_generator),
                    ("imputer",imputer)
                ]
            )
            return processor

        except Exception as e:
            raise CustomException(e,sys)



    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Entered in Initiate Data Transformation Method of Data Transformation Class")
        try:
            logging.info("Starting Data Transformation")
            train_df = pd.read_csv(self.data_validation_artifact.valid_train_filepath)
            test_df = pd.read_csv(self.data_validation_artifact.valid_test_filepath)

            # training Dataframe
            input_features_train_df = train_df.drop(columns=[Target_Feature])
            target_feature_train_df = train_df[Target_Feature].replace(-1,0)

            # testing Dataframe
            input_features_test_df = test_df.drop(columns=[Target_Feature])
            target_feature_test_df = test_df[Target_Feature].replace(-1,0)

            # Using Processor to create preprocessed array for test and train_dfs
            preprocessor = self.get_data_transformer_object()
            preprocessor_object = preprocessor.fit(input_features_train_df)
            transformed_input_train_features= preprocessor_object.transform(input_features_train_df) # array format
            transformed_input_test_features= preprocessor_object.transform(input_features_test_df) # array format

            # Using numpy to combine arr with np.array(Dataframe)
            train_arr = np.c_[transformed_input_train_features,np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_features,np.array(target_feature_test_df)]

            # Saving Train and Test Array & Preprocesser Object
            store_numpy_array(self.data_transformation_config.transformed_train_filepath, train_arr)
            store_numpy_array(self.data_transformation_config.transformed_test_filepath, test_arr)
            save_object(self.data_transformation_config.transformed_object_filepath, preprocessor_object)
            save_object("final_models/preprocessor.pkl",preprocessor_object)

            # Preparing Artifacts
            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_filepath= self.data_transformation_config.transformed_train_filepath,
                transformed_test_filepath= self.data_transformation_config.transformed_test_filepath,
                transformed_object_filepath= self.data_transformation_config.transformed_object_filepath
            )

            return data_transformation_artifact
            
        except Exception as e:
            raise CustomException(e,sys)