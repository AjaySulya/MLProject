from multiprocessing.util import info
import os 
import sys
import pandas as pd
from src.exception import CustomException
from src.logger import logging

from sklearn.model_selection import train_test_split

from dataclasses import dataclass # this will use to create a class variable 
## this is for checking everything working fine or not 
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig
# this for testing purpose 

@dataclass # provides consise way to define classes which are primarily used to store and manage data , It significantly reduces boilerplate code by automatically generating methods like __init__,__repr__, and __eq__ based on the class attributes.
class DataIngestionConfig:
    # these are the inputs which are giving to data ingestion component,
    # data ingestion components know where to save the train path and test path because of this file path
    train_data_path: str = os.path.join('artifacts','train.csv')
    test_data_path: str= os.path.join('artifacts','test.csv')
    raw_data_path: str = os.path.join('artifacts','data.csv')

class DataIngestion:
    # whenever i call this class , it save this config in the variables , 
    def __init__(self):
        # this variable consists the above three file paths or values
        self.ingestion_config = DataIngestionConfig()
        
    def initiate_data_ingestion(self):
        # generate longging message    
        logging.info("Entered the data ingestion method or component")
        # use try except block to handle the exception 
        try:
            ## read the dataset from the different sources like csv, mongodb, api etc.
            df = pd.read_csv('notebook\data\stud.csv') # here you can read from mongg db and other sources as well 
            logging.info('Read the dataset as dataframe')
            # I am creating a directory to save the train , test and raw data where the directory name is artificts
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok = True) # exist_ok = True will not raise an error if the directory already exists
            
            # for the save the raw data path
            df.to_csv(self.ingestion_config.raw_data_path,index = False,header = True) # write the dataframe to csv file with headers but without index , at the given path
            
            logging.info("Train and test split initiated")
            train_set,test_set = train_test_split(df,test_size = 0.2,random_state = 42) # split the data into train and test set with 80% train and 20% test 
            # save the train and test data to the respective paths
            train_set.to_csv(self.ingestion_config.train_data_path,index = False,header = True) # write the train set to csv file with headers but without index
            # same for the test set 
            test_set.to_csv(self.ingestion_config.test_data_path,index = False,header = True) # write the test set to csv file with headers but without index
            logging,info("Ingestion of the data is completed")
            
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            
            ) # because we need these information for my data transformation  component , so we are returning these paths
            
            
        except Exception as e:
            raise CustomException(e,sys) # sys module is use let us interact with the interpreter and get the information about the exception  
        ##### sys is bridge between the python code and the runtime environment , it provides the information about the exception that occurred in the code 


# this is for testing purpose
if __name__=="__main__":
    # here we first ingest data and then transform them right. 
    obj = DataIngestion()
    train_data , test_data = obj.initiate_data_ingestion() # this will call the initiate_data_ingestion method and execute the code inside it 
    data_transformation = DataTransformation() # here i making the instance of DataTransformation class 
    # by reference this object i call the initialize data transformation method 
    data_transformation.initiate_data_transformation(train_data,test_data)  # and data transformation method take two parameteres one is train_data , and test_data by using those data is initialize the data transformation
           