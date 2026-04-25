import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import os
import sys

def create_synthetic_data(filename="loan_data.csv"):
    """Generates a synthetic dataset for loan approval prediction."""
    np.random.seed(42)
    n_samples = 1000
    
    # Features
    income = np.random.randint(20000, 150000, n_samples)
    credit_score = np.random.randint(300, 850, n_samples)
    employment_status = np.random.choice(['Unemployed', 'Employed', 'Self-Employed'], n_samples, p=[0.1, 0.7, 0.2])
    loan_amount = np.random.randint(5000, 50000, n_samples)
    
    # Target Logic: Higher income, higher credit score, employed -> higher chance of approval
    score = (income / 50000) + (credit_score / 300) - (loan_amount / 20000)
    score += np.where(employment_status == 'Employed', 1, 0)
    score += np.where(employment_status == 'Self-Employed', 0.5, 0)
    score -= np.where(employment_status == 'Unemployed', 1.5, 0)
    
    # Define Approval Threshold
    target = np.where(score > 3.0, 'Approved', 'Rejected')
    
    df = pd.DataFrame({
        'Income': income,
        'CreditScore': credit_score,
        'EmploymentStatus': employment_status,
        'LoanAmount': loan_amount,
        'LoanStatus': target
    })
    
    df.to_csv(filename, index=False)
    print(f"[*] Synthetic dataset created and saved to {filename}")
    return df

def preprocess_and_train(df):
    """Preprocesses data and trains a Logistic Regression model."""
    print("\n--- Data Preprocessing ---")
    
    # 1. Handle missing values (Drop NA for simplicity)
    initial_shape = df.shape[0]
    df.dropna(inplace=True)
    if initial_shape != df.shape[0]:
        print(f"Dropped {initial_shape - df.shape[0]} rows with missing values.")
    
    # 2. Encode Categorical Data
    le_employment = LabelEncoder()
    # Handle unseen labels carefully in real-world, but we use known labels here
    df['EmploymentStatus'] = le_employment.fit_transform(df['EmploymentStatus'])
    
    le_target = LabelEncoder()
    df['LoanStatus'] = le_target.fit_transform(df['LoanStatus'])
    
    # Separate Features and Target
    X = df[['Income', 'CreditScore', 'EmploymentStatus', 'LoanAmount']]
    y = df['LoanStatus']
    
    # Train-test split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Feature Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("--- Training Logistic Regression Model ---")
    model = LogisticRegression(random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Predictions
    y_pred = model.predict(X_test_scaled)
    
    # Evaluation
    accuracy = accuracy_score(y_test, y_pred)
    
    print("\n--- Model Evaluation ---")
    print(f"Accuracy: {accuracy * 100:.2f}%\n")
    
    # Inverse transform to get true class names for the report
    classes = np.unique(y_test)
    target_names = le_target.inverse_transform(classes)
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=target_names))
    
    return model, scaler, le_employment, le_target

def predict_new_applicant(model, scaler, le_employment, le_target):
    """Takes user input to predict loan approval."""
    print("\n--- Predict Loan Approval for New Applicant ---")
    try:
        income = float(input("Enter Income (e.g., 50000): "))
        credit_score = float(input("Enter Credit Score (300-850): "))
        
        emp_status_input = input("Enter Employment Status (Employed/Unemployed/Self-Employed): ").strip().title()
        if emp_status_input not in le_employment.classes_:
            print(f"Invalid Employment Status! Please choose from: {', '.join(le_employment.classes_)}")
            return
            
        loan_amount = float(input("Enter Loan Amount: "))
        
        # Transform inputs
        emp_status_encoded = le_employment.transform([emp_status_input])[0]
        input_data = np.array([[income, credit_score, emp_status_encoded, loan_amount]])
        
        # Scale inputs
        input_scaled = scaler.transform(input_data)
        
        # Predict
        prediction_encoded = model.predict(input_scaled)[0]
        prediction_label = le_target.inverse_transform([prediction_encoded])[0]
        
        print(f"\n=> Predicted Loan Status: {prediction_label}")
        
    except ValueError:
        print("Invalid numerical input. Please enter valid numbers for income, credit score, and loan amount.")
    except Exception as e:
        print(f"An error occurred during prediction: {e}")

if __name__ == "__main__":
    dataset_file = "loan_data.csv"
    
    # Load or generate dataset
    if not os.path.exists(dataset_file):
        print(f"Dataset '{dataset_file}' not found. Generating synthetic data...")
        df = create_synthetic_data(dataset_file)
    else:
        print(f"Loading existing dataset from '{dataset_file}'...")
        try:
            df = pd.read_csv(dataset_file)
        except Exception as e:
            print(f"Failed to read {dataset_file}: {e}")
            sys.exit(1)
            
    # Check if necessary columns exist
    required_columns = ['Income', 'CreditScore', 'EmploymentStatus', 'LoanAmount', 'LoanStatus']
    if not all(col in df.columns for col in required_columns):
        print(f"Error: The dataset must contain the following columns: {', '.join(required_columns)}")
        sys.exit(1)
        
    # Train the model and get preprocessors
    model, scaler, le_employment, le_target = preprocess_and_train(df)
    
    # Interactive Console Loop
    while True:
        try:
            choice = input("\nDo you want to predict a new applicant's loan status? (y/n): ").strip().lower()
            if choice == 'y':
                predict_new_applicant(model, scaler, le_employment, le_target)
            elif choice == 'n':
                print("Exiting...")
                break
            else:
                print("Please enter 'y' or 'n'.")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
