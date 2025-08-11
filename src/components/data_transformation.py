# import some necessary libraries
import os
from dataclasses import dataclass
import numpy as np
import pandas as pd
import sys

# for saving object
from src.utils import save_object
# Data Transformation Configuration

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline

# impute configuration class # it handle the missing values fill with the mean/median and mode 
from sklearn.impute import SimpleImputer

# for exception handling
from src.exception import CustomException

# logging configuration
from src.logger import logging

@dataclass # dataclass to store configuration related to data transformation
class DataTransformationConfig: # for storing the all configuration related to data transformation
    # define the path for the transformed data
    # on this path i have to save the preprocessed dataset as preprocessor.pkl
    preprocessor_obj_file_path = os.path.join('artifacts',"preprocessor.pkl") # input for the data transformation component
    
    
class DataTransformation:
    # class handle all the preprocessing steps(scaling , encoding, imputing) for both training and testing data and saved fitted transform object for future use 
    def __init__(self):
        # DataTransformation Constructor : initialize the configuration for savinig the preprocessor.pkl file 
        self.data_transformation_config = DataTransformationConfig() # initialize the configuration
        
        
    def get_data_transformer_object(self):
        
        # this function is responsible for data transformation based on features types
        # to create pickle file for the preprocessor object
        """
        This method creates a data transformation pipeline that includes:
        - Imputation for numerical features
        - Standard scaling for numerical features
        - One-hot encoding for categorical features
        """
        #logging start for the data transformation  
        
        logging.info("Data Transformation initiated")
        
        # exception handling 
        try:
            # define numerical features and categorical features
            numerical_features =  ['writing_score', 'reading_score']  # example numerical features
            categorical_features = [
                                    'gender',
                                    'race_ethnicity',
                                    'parental_level_of_education',
                                    'lunch',
                                    'test_preparation_course'
            ]
            
            """        . Apply multiple steps in one go
                        Numeric data often needs:  Missing value handling (SimpleImputer → fill with mean/median)
                        Scaling (StandardScaler, MinMaxScaler)
                        Sometimes feature engineering (log transform, polynomial features, etc.)
                        A numerical pipeline chains these steps together:"""
                        # we are creting the pipeline for the handling the missing values and scaling the numerical features
                        # this pipeline  will be use to transform the numerical features on the training and testing data 
            num_pipeline = Pipeline(
                steps = [
                    ("imputer",SimpleImputer(strategy = 'median')), # impute missing values with median
                    ("scaler",StandardScaler()) # scale the numerical features
                ]
            )
            
            # In this categorical pipeline, we handle missing values by replacing them with the  mode (most frequent value) of each categgorical feature.
            # then we apply one-hot encoding to convert categorical variables into a format that can be provided to ML algorithms to do a better job in prediction.
            
            cat_pipeline = Pipeline(
                steps = [
                    ("Imputer",SimpleImputer(strategy = 'most_frequent')), # impute the missing values with most_frequent value 
                    ("one_hot_encoder",OneHotEncoder(handle_unknown = 'ignore')),
                    ("scaler",StandardScaler(with_mean = False)) # scaling categorical features 
                ]
            )
            logging.info(f"Categorical columns {categorical_features}")
            logging.info(f"NUmerical columns {numerical_features}")
            # combine the numerical and categorical pipelines into a single ColumnTransformer
            preprocessor = ColumnTransformer(
                transformers = [
                    ("num_pipeline",num_pipeline,numerical_features), # apply numerical pipeline to numerical features
                    ("cat_pipeline",cat_pipeline,categorical_features) # apply categorical pipeline to categorical features
                ]
            )
            
            return preprocessor # return the preprocessor object which will be used to tranform the data 
        except Exception as e:
            raise CustomException(e,sys)
        
         
    def initiate_data_transformation(self,train_path,test_path): # train_path and test_path are the paths of the train and test data , which are passed from the data ingestion component
        # this function is responsible for initiating the data transformation process
        logging.info("Data Transformation started")
        # handle the exception            
        try:
            train_df = pd.read_csv(train_path) # read the train data from the given path
            test_df = pd.read_csv(test_path) # read the test data from the given path
            
            logging.info("Read the train and test data as dataframes")                
            preprocessor_obj = self.get_data_transformer_object() # get the preprocessor object 
            target_column_name = 'math_score' # target column name
            numerical_features = ['writing_score', 'reading_score'] # numerical features
            
            # split the trainig data into input and target 
            input_features_train_df = train_df.drop(columns = [target_column_name],axis = 1) # independent features
            target_feature_train_df = train_df[target_column_name]
            
            # split the test data into input and target 
            input_features_test_df = test_df.drop(columns = [target_column_name],axis = 1) # independent features
            target_feature_test_df = test_df[target_column_name]
            
            # logging 
            logging.info(f"Apply the preprocessing object on training dataframe and test dataframe.")
            
            input_features_train_arr = preprocessor_obj.fit_transform(input_features_train_df)
            input_features_test_arr = preprocessor_obj.transform(input_features_test_df)
            # np.c_[] is in numpy , column concatination shortcut
            # join the preprocessed features and target values into one array so  they can stored and passed around together
        
            '''prevent mismatch later, pipeline standardization, convenience for debugging'''
            
            train_arr = np.c_[
                input_features_train_arr,np.array(target_feature_train_df) # train_arr , train_df join horizontally (column-wise)
            ]
            test_arr = np.c_[
                input_features_test_arr,np.array(target_feature_test_df) 
            ]
            logging.info(f"Saved preprocessed object")
            
            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessor_obj
            )
            
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path, # pickle file path 
            )
        except Exception as e:
            raise CustomException(e,sys)    
            