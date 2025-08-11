# comman functionalitis which use by entire project
import os 
import sys
import numpy as np 
import pandas as pd
import dill
# model evaluation , performance metrics
from sklearn.metrics import r2_score
from src.exception import CustomException

def save_object(file_path,obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok = 1)
        
        with open(file_path, 'wb',) as file_obj:
            dill.dump(obj,file_obj)
    except Exception as e:
        raise CustomException(e,sys)
    
    
# function for evaluating the model performation 
def evaluate_models(X_train,y_train,X_test,y_test,models):
    try:
        report = {}
        for model_name , model in models.items():
            model.fit(X_train,y_train)                  # fit the trainig data 
            y_train_pred = model.predict(X_train)       # prediction of model on training data
            y_test_pred = model.predict(X_test)         # prediction of model on testing data
            # model performance
            train_model_score = r2_score(y_train,y_train_pred)  # r2 score for the training data set
            test_model_score = r2_score(y_test,y_test_pred)     # r2 score for the testing data set
            
            # store the test score in dictionay
            report[model_name]  =  test_model_score
            
            return report
    except Exception as e:
        raise CustomException(e,sys)    