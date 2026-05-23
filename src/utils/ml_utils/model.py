import os,sys

from src.utils.main_utils import save_object

from src.exception.exception import CustomException
from src.logger.log import logging

class Model:
    def __init__(self,preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            try:
                raise CustomException(e,sys)
            except CustomException as ce:
                print(ce)

    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            try:
                raise CustomException(e,sys)
            except CustomException as ce:
                print(ce)