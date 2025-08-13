# import basic libraries
import sys 
import os
import pandas as pd
# handle the exceptions 
from src.exception import CustomException
# for the load pickle object for predictions 
from src.utils import load_object


class PredictPipeline:
    def __init__(self):
        pass
    def predict(self,features):
        try:
            model_path = 'artifacts\\model.pkl'
            preprocessor_path = 'artifacts\\preprocessor.pkl'
            # load the data for predictions 
            model = load_object(file_path = model_path)
            preprocessor = load_object(file_path = preprocessor_path)
            # scaled the input features 
            
            # if there is not model and preprocessor then do this by default 
            if model is None or preprocessor is None:
                mock_prediction = (features['reading_score'].iloc[0] + features['writing_score'].loc[0] / 2) 
                return mock_prediction
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            return preds
        except Exception as e:
            raise CustomException(e,sys)
        # return the preds 
        
        
        
# customedata class is responshible for the mapping all the input which we are giving through the html page to the backend with this particular values 

class CustomData:
    def __init__(self,
                 gender: str,
                 race_ethnicity: str,
                 parental_level_of_education,
                 lunch: str,
                 test_preparation_course: str,
                 reading_score: int,
                 writing_score: int):
        # asigning the values of global and local variable
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.lunch = lunch
        self.parental_level_of_education = parental_level_of_education
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score  = writing_score
        
        
    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                    "gender" : [self.gender],
                    "race_ethnicity" : [self.race_ethnicity],
                    "parental_level_of_education" : [self.parental_level_of_education],
                    "lunch" : [self.lunch],
                    "test_preparation_course" : [self.test_preparation_course],
                    "reading_score" : [self.reading_score],
                    "writing_score" : [self.writing_score]
                }
                
            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            raise CustomException(e,sys)    