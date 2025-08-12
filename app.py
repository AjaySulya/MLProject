# for the flask app
from flask import Flask, request,render_template
# basic libraries 
import numpy as np
import pandas as pd

# for the scalling the features
# from sklearn.preprocessing import StandardScaler
# for the mapping the data and doing the predictions
from src.pipeline.predict_pipeline import CustomData,PredictPipeline

application = Flask(__name__)

app = application # instance of the application file 

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# route for the prediction data
@app.route('/predictdata',methods = ['GET','POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html') # it's basical a form to fill the input features 
    
    else:
         # here prediction should be done 
         # here i am calling the CustomData class for the mapping the html input to the back end data frame 
        data = CustomData(
            gender = request.form.get('gender'),
            race_ethnicity= request.form.get('race_ethnicity'),
            parental_level_of_education= request.form.get('parental_level_of_education'),
            lunch = request.form.get('lunch'),
            test_preparation_course= request.form.get('test_preparation_course'),
            reading_score= request.form.get('reading_score'),
            writing_score = request.form.get('writing_score')
        )
        
        pred_df = data.get_data_as_data_frame()
        # i can see the how my data look like in data frame 
        print(pred_df)
        
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)
        
        return render_template('home.html',results = results[0])
    
# for testing purpose 
if __name__=="__main__":
    app.run(host="0.0.0.0",debug = True)    