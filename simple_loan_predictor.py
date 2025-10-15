#!/usr/bin/env python3
"""
Simple Loan Default Predictor
Pure Python implementation using the actual CSV dataset
"""

import math
import csv
import random

# Model parameters (extracted from trained logistic regression)
COEFFICIENTS = {
    'age': 0.0393,
    'campaign': -0.2032,
    'pdays': -0.2790,
    'previous': 0.1427,
    'contact_cellular': 0.4383,
    'month_mar': 0.1977,
    'month_oct': 0.1847,
    'default_no': 0.1843,
    'job_management': -0.0175,
    'job_technician': -0.0091,
    'marital_married': -0.0181,
    'education_university.degree': 0.0540,
    'housing_no': 0.0093,
    'loan_no': 0.0198
}

INTERCEPT = -0.3273
OPTIMAL_THRESHOLD = 0.6

def load_csv_data(filename, sample_size=10):
    """
    Load data from CSV file and return sample records
    
    Args:
        filename (str): Path to CSV file
        sample_size (int): Number of random samples to return
        
    Returns:
        list: Sample data records with headers
    """
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            all_data = list(reader)
            
        # Get random sample
        sample_data = random.sample(all_data, min(sample_size, len(all_data)))
        
        print(f"✓ Loaded {len(all_data)} records from {filename}")
        print(f"✓ Selected {len(sample_data)} random samples for prediction")
        
        return sample_data, all_data
        
    except FileNotFoundError:
        print(f"❌ CSV file '{filename}' not found")
        return [], []
    except Exception as e:
        print(f"❌ Error loading CSV: {str(e)}")
        return [], []

def convert_csv_row_to_features(row):
    """
    Convert CSV row to feature dictionary for prediction
    
    Args:
        row (dict): CSV row data
        
    Returns:
        dict: Features for prediction
    """
    features = {}
    
    # Convert relevant columns to features
    features['age'] = float(row.get('age', 0))
    features['campaign'] = float(row.get('campaign', 0))
    features['pdays'] = float(row.get('pdays', 0))
    features['previous'] = float(row.get('previous', 0))
    features['contact_cellular'] = float(row.get('contact_cellular', 0))
    features['month_mar'] = float(row.get('month_mar', 0))
    features['month_oct'] = float(row.get('month_oct', 0))
    features['default_no'] = float(row.get('default_no', 0))
    features['job_management'] = float(row.get('job_management', 0))
    features['job_technician'] = float(row.get('job_technician', 0))
    features['marital_married'] = float(row.get('marital_married', 0))
    features['education_university.degree'] = float(row.get('education_university.degree', 0))
    features['housing_no'] = float(row.get('housing_no', 0))
    features['loan_no'] = float(row.get('loan_no', 0))
    
    return features

def predict_loan_default(customer_data):
    """
    Predict loan default probability for a customer
    
    Args:
        customer_data (dict): Customer information
        
    Returns:
        dict: Prediction results
    """
    
    # Calculate linear combination
    score = INTERCEPT
    
    for feature, coefficient in COEFFICIENTS.items():
        value = customer_data.get(feature, 0)
        score += coefficient * value
    
    # Apply logistic function to get probability
    probability = 1 / (1 + math.exp(-score))
    
    # Make decision based on optimal threshold
    prediction = 1 if probability > OPTIMAL_THRESHOLD else 0
    
    # Determine risk level
    if probability < 0.2:
        risk_level = "Low Risk"
    elif probability < 0.5:
        risk_level = "Medium Risk"
    elif probability < 0.8:
        risk_level = "High Risk"
    else:
        risk_level = "Very High Risk"
    
    # Make recommendation
    recommendation = "REVIEW/REJECT" if prediction == 1 else "APPROVE"
    
    return {
        'probability': probability,
        'predicted_default': prediction,
        'risk_level': risk_level,
        'recommendation': recommendation
    }
    """
    Predict loan default probability for a customer
    
    Args:
        customer_data (dict): Customer information
        
    Returns:
        dict: Prediction results
    """
    
    # Calculate linear combination
    score = INTERCEPT
    
    for feature, coefficient in COEFFICIENTS.items():
        value = customer_data.get(feature, 0)
        score += coefficient * value
    
    # Apply logistic function to get probability
    probability = 1 / (1 + math.exp(-score))
    
    # Make decision based on optimal threshold
    prediction = 1 if probability > OPTIMAL_THRESHOLD else 0
    
    # Determine risk level
    if probability < 0.2:
        risk_level = "Low Risk"
    elif probability < 0.5:
        risk_level = "Medium Risk"
    elif probability < 0.8:
        risk_level = "High Risk"
    else:
        risk_level = "Very High Risk"
    
    # Make recommendation
    recommendation = "REVIEW/REJECT" if prediction == 1 else "APPROVE"
    
    return {
        'probability': probability,
        'predicted_default': prediction,
        'risk_level': risk_level,
        'recommendation': recommendation
    }

def demo_with_csv_data():
    """Demonstrate the predictor using actual CSV data"""
    
    print("=== Loan Default Predictor - Using CSV Data ===")
    print("Model Accuracy: 78.8%")
    print("Optimal Threshold: 60%\n")
    
    # Load CSV data
    sample_data, all_data = load_csv_data('loan_detection.csv', sample_size=5)
    
    if not sample_data:
        print("Could not load CSV data. Using demo data instead.")
        demo()  # Fall back to original demo
        return
    
    print("\nPredictions on Real CSV Data:")
    print("-" * 80)
    print(f"{'Row #':<8} {'Age':<5} {'Campaign':<9} {'Probability':<12} {'Risk Level':<15} {'Decision':<12} {'Actual'}")
    print("-" * 80)
    
    correct_predictions = 0
    
    for i, row in enumerate(sample_data, 1):
        # Convert CSV row to features
        features = convert_csv_row_to_features(row)
        
        # Make prediction
        result = predict_loan_default(features)
        
        # Get actual result from CSV
        actual_default = int(row.get('Loan_Status_label', 0))
        actual_text = "Default" if actual_default == 1 else "No Default"
        
        # Check if prediction matches actual
        predicted_default = result['predicted_default']
        is_correct = predicted_default == actual_default
        if is_correct:
            correct_predictions += 1
        
        # Display results
        prob_str = f"{result['probability']:.1%}"
        age = int(float(row.get('age', 0)))
        campaign = int(float(row.get('campaign', 0)))
        
        status_marker = "✓" if is_correct else "✗"
        
        print(f"{i:<8} {age:<5} {campaign:<9} {prob_str:<12} {result['risk_level']:<15} {result['recommendation']:<12} {actual_text} {status_marker}")
    
    accuracy = (correct_predictions / len(sample_data)) * 100
    print(f"\nSample Accuracy: {correct_predictions}/{len(sample_data)} ({accuracy:.1f}%)")
    
    # Show dataset statistics
    print(f"\n📊 Dataset Statistics:")
    print(f"Total records: {len(all_data):,}")
    
    if all_data:
        default_count = sum(1 for row in all_data if int(row.get('Loan_Status_label', 0)) == 1)
        default_rate = (default_count / len(all_data)) * 100
        print(f"Default rate: {default_count:,}/{len(all_data):,} ({default_rate:.1f}%)")
        
        # Age statistics
        ages = [int(float(row.get('age', 0))) for row in all_data if row.get('age')]
        if ages:
            avg_age = sum(ages) / len(ages)
            print(f"Average age: {avg_age:.1f} years")
            print(f"Age range: {min(ages)} - {max(ages)} years")

def demo():
    """Original demo function with hardcoded test cases"""
    
    print("=== Simple Loan Default Predictor ===")
    print("Model Accuracy: 78.8%")
    print("Optimal Threshold: 60%\n")
    
    # Test cases
    customers = [
        {
            'name': 'John (Low Risk)',
            'data': {
                'age': 45,
                'campaign': 1,
                'contact_cellular': 1,
                'job_management': 1,
                'marital_married': 1,
                'education_university.degree': 1,
                'default_no': 1,
                'housing_no': 1,
                'loan_no': 1
            }
        },
        {
            'name': 'Sarah (Medium Risk)',
            'data': {
                'age': 28,
                'campaign': 3,
                'contact_cellular': 1,
                'month_mar': 1,
                'job_technician': 1,
                'default_no': 1
            }
        },
        {
            'name': 'Mike (High Risk)',
            'data': {
                'age': 22,
                'campaign': 5,
                'contact_cellular': 1,
                'month_oct': 1,
                'default_no': 0  # Has previous default
            }
        }
    ]
    
    print("Customer Risk Assessment:")
    print("-" * 70)
    print(f"{'Name':<20} {'Probability':<12} {'Risk Level':<15} {'Decision'}")
    print("-" * 70)
    
    for customer in customers:
        result = predict_loan_default(customer['data'])
        prob_str = f"{result['probability']:.1%}"
        print(f"{customer['name']:<20} {prob_str:<12} {result['risk_level']:<15} {result['recommendation']}")
    
    print("\nMost Important Risk Factors:")
    print("+ contact_cellular: Being contacted via cellular phone (+43.8%)")
    print("- pdays: Days since last contact (-27.9%)")
    print("+ month_mar: Application in March (+19.8%)")
    print("+ month_oct: Application in October (+18.5%)")
    print("+ default_no: No previous default (+18.4%)")
    """Demonstrate the loan predictor with example customers"""
    
    print("=== Simple Loan Default Predictor ===")
    print("Model Accuracy: 78.8%")
    print("Optimal Threshold: 60%\n")
    
    # Test cases
    customers = [
        {
            'name': 'John (Low Risk)',
            'data': {
                'age': 45,
                'campaign': 1,
                'contact_cellular': 1,
                'job_management': 1,
                'marital_married': 1,
                'education_university.degree': 1,
                'default_no': 1,
                'housing_no': 1,
                'loan_no': 1
            }
        },
        {
            'name': 'Sarah (Medium Risk)',
            'data': {
                'age': 28,
                'campaign': 3,
                'contact_cellular': 1,
                'month_mar': 1,
                'job_technician': 1,
                'default_no': 1
            }
        },
        {
            'name': 'Mike (High Risk)',
            'data': {
                'age': 22,
                'campaign': 5,
                'contact_cellular': 1,
                'month_oct': 1,
                'default_no': 0  # Has previous default
            }
        }
    ]
    
    print("Customer Risk Assessment:")
    print("-" * 70)
    print(f"{'Name':<20} {'Probability':<12} {'Risk Level':<15} {'Decision'}")
    print("-" * 70)
    
    for customer in customers:
        result = predict_loan_default(customer['data'])
        prob_str = f"{result['probability']:.1%}"
        print(f"{customer['name']:<20} {prob_str:<12} {result['risk_level']:<15} {result['recommendation']}")
    
    print("\nMost Important Risk Factors:")
    print("+ contact_cellular: Being contacted via cellular phone (+43.8%)")
    print("- pdays: Days since last contact (-27.9%)")
    print("+ month_mar: Application in March (+19.8%)")
    print("+ month_oct: Application in October (+18.5%)")
    print("+ default_no: No previous default (+18.4%)")

def predict_new_customer():
    """Example of predicting for a new customer"""
    
    print("\n=== New Customer Assessment ===")
    
    # Example new customer
    new_customer = {
        'age': 35,
        'campaign': 2,
        'contact_cellular': 1,
        'job_management': 1,
        'marital_married': 1,
        'education_university.degree': 1,
        'default_no': 1,
        'housing_no': 1,
        'loan_no': 1
    }
    
    result = predict_loan_default(new_customer)
    
    print("Customer Profile:")
    print(f"- Age: {new_customer['age']}")
    print(f"- Job: Management")
    print(f"- Marital Status: Married")
    print(f"- Education: University Degree")
    print(f"- Previous Default: No")
    
    print(f"\nRisk Assessment:")
    print(f"- Default Probability: {result['probability']:.1%}")
    print(f"- Risk Level: {result['risk_level']}")
    print(f"- Recommendation: {result['recommendation']}")
    
    if result['probability'] < 0.3:
        advice = "Low risk - approve with standard terms"
    elif result['probability'] < 0.6:
        advice = "Medium risk - consider approval with monitoring"
    else:
        advice = "High risk - require additional documentation or collateral"
    
    print(f"- Business Advice: {advice}")

if __name__ == "__main__":
    demo_with_csv_data()  # Use CSV data first
    predict_new_customer()
    
    print("\n" + "="*50)
    print("✅ Simple loan predictor completed!")
    print("✅ Using actual CSV data for predictions")
    print("✅ Created by Japneet Singh Anand")