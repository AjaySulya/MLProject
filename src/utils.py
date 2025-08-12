# comman functionalitis which use by entire project
import os 
import sys
import numpy as np 
import pandas as pd
import dill
from sklearn.model_selection import GridSearchCV
# model evaluation , performance metrics
from sklearn.metrics import r2_score

# For the hyperparamter tuning
from src.exception import CustomException
from src.logger import logging

def save_object(file_path,obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok = 1)
        
        with open(file_path, 'wb',) as file_obj:
            dill.dump(obj,file_obj)
    except Exception as e:
        raise CustomException(e,sys)
    
    
# function for evaluating the model performation 
def evaluate_models(X_train,y_train,X_test,y_test,models,params):
    try:
        report = {}
        for model_name , model in models.items():
            
            model.fit(X_train,y_train)  # fit the trainig data 
            param = params[model_name] # getting the parameters and after i am use the values of perticular model 
            
            gs = GridSearchCV(model,param,cv = 3)
            # train the model with using the hyperparameter
            gs.fit(X_train,y_train) # train our model 
            logging.info("Model Trained by GridSearchCV.")
            # setting the best parameters required for the best performance 
            model.set_params(**gs.best_params_) # for each perticular model i am setting there best parameteres
            model.fit(X_train,y_train) # then again i am train my model with using those hyperparametes 
            
            y_train_pred = model.predict(X_train)       # prediction of model on training data
            y_test_pred = model.predict(X_test)         # prediction of model on testing data
            # model performance
            # train_model_score = r2_score(y_train,y_train_pred)  # r2 score for the training data set
            test_model_score = r2_score(y_test,y_test_pred)     # r2 score for the testing data set
            
            # store the test score in dictionay
            report[model_name]  =  test_model_score
            
            return report
    except Exception as e:
        raise CustomException(e,sys)    