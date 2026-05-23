import os,sys
import numpy as np
import pandas as pd


from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.svm import SVC
from xgboost import XGBClassifier

from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import (
    DataTransformationArtifact,
    ClassificationMetricsArtifact, 
    ModelTrainerArtifact
)

from src.utils.ml_utils.model import Model
from src.utils.ml_utils.classification_metric import get_classification_score
from src.utils.main_utils import load_numpy_array, evaluate_models, load_object, save_object, write_yaml_file

from src.logger.log import logging
from src.exception.exception import CustomException

import mlflow
import dagshub
dagshub.init(repo_owner='Akshat-WorkHub', repo_name='NetworkSecurity', mlflow=True)


class Model_Trainer:
    def __init__(self,model_trainer_config: ModelTrainerConfig, transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)

    def track_mlflow(self,best_model, classification_metric):
        with mlflow.start_run():
            f1_score = classification_metric.f1_score
            precision_score = classification_metric.precision_score
            recall_score = classification_metric.recall_score

            mlflow.log_metric("f1_score",f1_score)
            mlflow.log_metric("precision_score",precision_score)
            mlflow.log_metric("recall_score",recall_score)
            mlflow.sklearn.log_model(best_model,"model")
            

            
    def train_model(self,X_train, y_train, X_test, y_test):
        try:
            models = {
                "Logistic Regression": LogisticRegression(max_iter=1000),
                "Decision Tree": DecisionTreeClassifier(),
                "Random Forest": RandomForestClassifier(),
                "AdaBoost": AdaBoostClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(),
                "XGBoost": XGBClassifier(),
                "SVM": SVC(probability=True)
            }

            params = {
                "Logistic Regression": {
                    "C": [0.1, 1.0, 10.0],
                    "solver": ["liblinear"]
                },
                "Decision Tree": {
                    "criterion": ["gini", "entropy"],
                    "max_depth": [5, 8, 15, 20],
                    "min_samples_split": [2, 5, 10]
                },
                "Random Forest": {
                    "n_estimators": [50, 100, 200],
                    "max_depth": [5, 8, 15],
                    "min_samples_split": [2, 5, 10],
                    "class_weight": ["balanced", None] # CRITICAL: This helps fix the "Blind" issue
                },
                "AdaBoost": {
                    "n_estimators": [50, 100, 200],
                    "learning_rate": [0.1, 0.5, 1.0]
                },
                "Gradient Boosting": {
                    "n_estimators": [100, 200],
                    "learning_rate": [0.1, 0.05],
                    "subsample": [0.7, 0.8, 1.0]
                },
                "XGBoost": {
                    "n_estimators": [100, 200],
                    "learning_rate": [0.1, 0.01],
                    "max_depth": [3, 5, 8]
                },
                "SVM": {
                    "C": [1], 
                    "kernel": ["rbf"]
                }
            }

            model_report : dict = evaluate_models(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test,models=models,params=params)


            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            best_model = models[best_model_name]
            y_train_pred = best_model.predict(X_train)
            y_test_pred = best_model.predict(X_test)

            classification_train_metric = get_classification_score(y_true=y_train,y_pred=y_train_pred)
            classification_test_metric = get_classification_score(y_true=y_test,y_pred=y_test_pred)

            ## Space for track experiments with ML - Flow 
            self.track_mlflow(best_model,classification_train_metric)
            self.track_mlflow(best_model,classification_test_metric)

            preprocessor = load_object(self.data_transformation_artifact.transformed_object_filepath)

            model_dir_path = os.path.dirname(self.model_trainer_config.final_trained_model_filepath)
            os.makedirs(model_dir_path,exist_ok=True)

            internship_model = Model(preprocessor,best_model)
            save_object(self.model_trainer_config.final_trained_model_filepath, internship_model)
            save_object("final_models/model.pkl",best_model)
            
            full_report = {
                "selected_model": best_model_name,
                "best_score": float(best_model_score),
                "best_hyperparameters": best_model.get_params(), # Extracts the winning GridSearchCV params
                "classification_metrics": {
                    "f1_score": float(classification_test_metric.f1_score),
                    "precision_score": float(classification_test_metric.precision_score),
                    "recall_score": float(classification_test_metric.recall_score)
                }
            }
            
            
            metric_yaml_path = os.path.join(model_dir_path, "test_metrics.yaml")
            write_yaml_file(filepath=metric_yaml_path, content=full_report)

            ## Model Trainer Artifact
            model_trainer_artifact = ModelTrainerArtifact(
                final_trained_model_filepath= self.model_trainer_config.final_trained_model_filepath,
                train_metric_artifact= classification_train_metric,
                test_metric_artifact= classification_test_metric
            )

            logging.info(f"Model Trainer Artifact : {model_trainer_artifact}")

            return model_trainer_artifact
        
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_model_training(self,) -> ModelTrainerArtifact:
        try:
            train_filepath = self.data_transformation_artifact.transformed_train_filepath
            test_filepath = self.data_transformation_artifact.transformed_test_filepath

            train_arr = load_numpy_array(train_filepath)
            test_arr = load_numpy_array(test_filepath)

            X_train, y_train, X_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1]
            )

            model = self.train_model(X_train,y_train,X_test,y_test)
            
        except Exception as e:
            raise CustomException(e,sys)
