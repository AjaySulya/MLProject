# for the flask app
from flask import Flask, request,render_template,jsonify
# basic libraries 
import numpy as np
import pandas as pd
# for tht customexception 
from src.exception import CustomException
# for the render deployment
import traceback
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
    


@app.route('/api/predict', methods=['POST'])
def api_predict():
    try:
        data = request.get_json()

        # Required fields
        required_fields = ['gender', 'ethnicity', 'parental_level_of_education',
                           'lunch', 'test_preparation_course', 'reading_score', 'writing_score']
        for field in required_fields:
            if field not in data or data[field] is None:
                return jsonify(success=False, error=f'Missing required field: {field}'), 400

        # Convert scores
        try:
            reading_score = float(data['reading_score'])
            writing_score = float(data['writing_score'])
        except ValueError:
            return jsonify(success=False, error='Invalid score values'), 400

        # Validate range
        if not (0 <= reading_score <= 100) or not (0 <= writing_score <= 100):
            return jsonify(success=False, error='Scores must be between 0 and 100'), 400

        # Prepare data
        custom_data = CustomData(
            gender=data['gender'],
            race_ethnicity=data['ethnicity'],
            parental_level_of_education=data['parental_level_of_education'],
            lunch=data['lunch'],
            test_preparation_course=data['test_preparation_course'],
            reading_score=reading_score,
            writing_score=writing_score
        )
        pred_df = custom_data.get_data_as_data_frame()

        # Predict
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)

        prediction_value = results[0] if hasattr(results, '__iter__') and not isinstance(results, str) else results

        return jsonify(
            success=True,
            prediction=round(float(prediction_value), 1),
            message='Prediction completed successfully'
        )

    except CustomException as e:
        print(f"Custom API prediction error: {e}")
        return jsonify(success=False, error='Model prediction error'), 500
    except Exception as e:
        print(f"API prediction error: {e}")
        return jsonify(success=False, error='Internal server error'), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Test if pipeline can be created
        pipeline = PredictPipeline()
        return jsonify({
            'status': 'healthy',
            'pipeline_loaded': True
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'pipeline_loaded': False
        }), 500   




    
     # for the render error logs 
@app.errorhandler(Exception)
def handle_error(e):
    print("ERROR:", e)
    traceback.print_exc()  # prints full error to Render logs
    return jsonify({"error": str(e)}), 500   
# for testing purpose 
if __name__=="__main__":
    app.run(host="0.0.0.0")    