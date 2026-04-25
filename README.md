# AI_ProblemSolvingproblem_RA2411026050022_RA2411026050057
# Loan Approval Prediction System

An end-to-end Machine Learning web application that predicts whether a loan applicant is approved or rejected based on their financial profile.

## Features
- **Machine Learning Model**: Uses Logistic Regression (from Scikit-Learn) to classify applicants.
- **Data Pipeline**: Automatically handles missing values and categorical data using Pandas and LabelEncoder.
- **Synthetic Data Generation**: Automatically generates a 1,000-sample mock dataset (`loan_data.csv`) if one does not exist.
- **RESTful API**: Includes a lightweight Python Flask backend that serves predictions.
- **Modern UI**: A responsive, glassmorphism-styled frontend built with HTML, Vanilla CSS, and JavaScript.

## Tech Stack
- **Backend**: Python 3.x, Flask
- **Data Science**: Pandas, NumPy, Scikit-Learn
- **Frontend**: HTML5, Vanilla CSS, JavaScript

## Installation
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/loan-approval-prediction.git
   cd loan-approval-prediction
   ```

2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Web Application (Recommended)
Launch the Flask backend server:
