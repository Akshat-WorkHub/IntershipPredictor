import os,sys
import pickle, yaml
import numpy as np
import json

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score # Use F1 or Accuracy for Classification

from src.exception.exception import CustomException
from src.logger.log import logging

def read_yaml_file(filepath: str) -> yaml:
    try:
        logging.info("Loading Schema YAML File .........\n")
        if not os.path.exists(filepath):
            raise Exception(f"File Doesn't Exist : {filepath}")
        
        
        with open(filepath,'r') as yaml_readObj:
            return yaml.safe_load(yaml_readObj)
        
    except Exception as e:
        raise CustomException(e,sys)
    
    
def write_yaml_file(filepath: str, content: str, replace: bool = False) -> None:
    try:
        logging.info("Fetching Schema YAML Filepath .........\n")
        if replace:
            if os.path.exists(filepath):
                os.remove(filepath)
        logging.info(f"Storing Drift Report in given path {filepath} .........\n")
        with open(filepath,'w') as yaml_writeObj:
            yaml.dump(content,yaml_writeObj)

    except Exception as e:
        raise CustomException(e,sys)
    
    
def load_numpy_array(filepath: str):
    try:
        logging.info("Loading Numpy Array File .........\n")
        if not os.path.exists(filepath):
            raise Exception(f"File Doesn't Exist : {filepath}")
        
        with open(filepath,'rb') as npArrayObj:
            return np.load(npArrayObj)

    except Exception as e:
        raise CustomException(e,sys)
    

def store_numpy_array(filepath: str, arr: np.array):
    try:
        logging.info("Fetching Numpy Array Filepath .........\n")
        arr_dir = os.path.dirname(filepath)
        os.makedirs(arr_dir,exist_ok=True)

        logging.info(f"Storing Numpy on given Filepath {filepath} .........\n")
        with open(filepath,'wb') as npArrayObj:
            np.save(npArrayObj, arr)

    except Exception as e:
        raise CustomException(e,sys)
    

def load_object(filepath: str):
    try:
        logging.info("Loading Saved Preprocessor (Imputer) File .........\n")
        if not os.path.exists(filepath):
            raise Exception(f"File Doesn't Exist : {filepath}")
        
        with open(filepath,'rb') as fileObj:
            return pickle.load(fileObj)

    except Exception as e:
        raise CustomException(e,sys)


def save_object(filepath: str, preprocessor: object):
    try:
        logging.info("Fetching Preprocessor Filepath .........\n")
        imputer_dir = os.path.dirname(filepath)
        os.makedirs(imputer_dir,exist_ok=True)

        logging.info(f"Storing Numpy on given Filepath {filepath} .........\n")
        with open(filepath,'wb') as fileObj:
            pickle.dump(preprocessor, fileObj)
    except Exception as e:
        raise CustomException(e,sys)


def evaluate_models(X_train, y_train, X_test, y_test, models, params) -> dict:
    try:
        report = dict()
        for i in range(len(list(models))):
            model_name = list(models.keys())[i]
            model = list(models.values())[i]
            param = params[model_name]

            # 1. Initialize Grid Search
            # scoring='f1' ensures we optimize for the right metric
            gs = GridSearchCV(model, param, cv=3, scoring='f1', n_jobs=-1, verbose=3)
            gs.fit(X_train, y_train)

            # 2. Get the already-trained best model
            best_tuned_model = gs.best_estimator_

            # 3. Predict using the best model
            y_test_pred = best_tuned_model.predict(X_test)

            # 4. Calculate Classification Score
            test_model_score = f1_score(y_test, y_test_pred)

            # Important: Update the original models dictionary with the tuned model
            # so Model_Trainer can grab the fitted version later
            models[model_name] = best_tuned_model
            
            report[model_name] = test_model_score
        
        return report

    except Exception as e:
        raise CustomException(e, sys)
    

