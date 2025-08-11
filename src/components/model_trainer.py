import os  # for let you interact with the operating system for tasks like handling files , directories , variables
import sys # work as bridge between the python code and runtime environment
from dataclasses import dataclass # dundare class for making those class which are store and manipulate the data 

# Algorithms for train model 
from sklearn.linear_model import ( 
                                  LinearRegression,
                                  Lasso,
                                  Ridge
                                  ) 

from sklearn.tree  import DecisionTreeRegressor 
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor

# Ensembke algorithms

from sklearn.ensemble import (
    AdaBoostRegressor,
    RandomForestRegressor,
    GradientBoostingRegressor
)

# Performantion Metrics for for the model evaluations 
from sklearn.metrics import r2_score

# for logging and exception handling 
from src.logger import logging
from src.exception import CustomException


# for all the common function i will import utils 
from src.utils import (save_object,
                       evaluate_models)


@dataclass
class ModelTrainerConfig: # this will give the input whatever i required while my model training
    # variable for storing the trained model file path
    trained_model_file_path = os.path.join("artifacts","model.pkl")
    
# another class for training the model , inside this class we will train the model 
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()   
    
    # this method is responsibale for the initializing the model trainer
    def initiate_model_trainer(self,train_array,test_array): # it take 3 positional arguments : train_arr , test_arr and preprocessor_path - where my actual pickle file is exist
        try:
            # here i will write my entire code for initialising the model trainer
            logging.info("Split training and testing input data")
            X_train,y_train,X_test,y_test = (train_array[:,:-1],
                                             train_array[:,-1],
                                             test_array[:,:-1],
                                             test_array[:,-1])   # split the train (X,y) and test (X,y) 
            
            # make a dictionary for the models and model name 
            models = {
                'Lasso Regression': Lasso(),
                'Linear Regression': LinearRegression(),
                'Decision Tree Regressor': DecisionTreeRegressor(),
                'K-Neighbors Regressor': KNeighborsRegressor(),
                'XGBoost Regressor': XGBRegressor(),
                'Random Forest Regressor': RandomForestRegressor(),
                'Gradient Boosting Regressor': GradientBoostingRegressor(),
                'AdaBoost Regressor': AdaBoostRegressor(),
                'Ridge Regression': Ridge()
            }
            # evaluate model is a function which i have created in utils (which is common for all) it take 5 parameters
            #model_report contains the r2_score for each models which i have specify above 
            model_report:dict = evaluate_models(X_train= X_train,y_train= y_train,
                                               X_test = X_test , y_test = y_test,
                                               models = models)
            
            # To get the best model from the dict
            best_model_score = max(sorted(model_report.values()))
            
            # To get the best model name from the dict
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]                                                            # here i am just say that select the whose value or index is best_model_score . that's it 
            
            best_model = models[best_model_name] 
            
            if best_model_score < 0.6 :
                raise CustomException("No Best Model Found")
            
            logging.info("Best Model found on both training and testing dataset.")
            
            save_object(
                file_path = self.model_trainer_config.trained_model_file_path,
                obj = best_model
            )
             
            predicted  = best_model.predict(X_test) 
            r2_square  = r2_score(y_test,predicted)
            
            return r2_square
        except Exception as e:
            raise CustomException(e,sys)      
    