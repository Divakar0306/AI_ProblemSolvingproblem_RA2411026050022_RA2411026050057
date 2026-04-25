import os
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from loan_approval import create_synthetic_data, preprocess_and_train

app = Flask(__name__)
CORS(app)

# Global variables to hold the trained model and preprocessors
model = None
scaler = None
le_employment = None
le_target = None

def initialize_model():
    global model, scaler, le_employment, le_target
    dataset_file = "loan_data.csv"
    
    # Load or generate dataset
    if not os.path.exists(dataset_file):
        print(f"Generating synthetic data at {dataset_file}...")
        df = create_synthetic_data(dataset_file)
    else:
        df = pd.read_csv(dataset_file)
        
    model, scaler, le_employment, le_target = preprocess_and_train(df)
    print("Model loaded successfully.")

# Initialize model at startup
initialize_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        income = float(data.get('income', 0))
        credit_score = float(data.get('credit_score', 0))
        emp_status = data.get('employment_status', '').strip().title()
        loan_amount = float(data.get('loan_amount', 0))
        
        # Validate employment status
        if emp_status not in le_employment.classes_:
            return jsonify({'error': 'Invalid employment status.'}), 400
            
        # Encode
        emp_status_encoded = le_employment.transform([emp_status])[0]
        input_data = np.array([[income, credit_score, emp_status_encoded, loan_amount]])
        
        # Scale
        input_scaled = scaler.transform(input_data)
        
        # Predict
        pred_encoded = model.predict(input_scaled)[0]
        pred_label = le_target.inverse_transform([pred_encoded])[0]
        
        return jsonify({'prediction': pred_label})
        
    except ValueError as ve:
        return jsonify({'error': 'Invalid input values. Please provide numbers for income, credit score, and loan amount.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
