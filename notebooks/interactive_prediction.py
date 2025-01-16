import pandas as pd
import joblib
from colorama import Fore, Style, init
import time

# Initialize colorama for colored text
init(autoreset=True)

# Load the trained model
try:
    model = joblib.load('../data/model.pkl')
    expected_features = model.feature_names_in_
except FileNotFoundError:
    print(Fore.RED + "Error: Model file not found. Ensure the path to 'model.pkl' is correct.")
    exit()
except Exception as e:
    print(Fore.RED + f"Unexpected error while loading the model: {str(e)}")
    exit()

def display_processing():
    """Simulates a processing delay with a loading animation."""
    print(Fore.GREEN + "Processing your data", end="")
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="")
    print("\n" + Style.RESET_ALL)

def predict_loan():
    """Main function for loan prediction."""
    while True:
        try:
            # Display a styled header
            print(Fore.CYAN + "=" * 50)
            print(Fore.MAGENTA + Style.BRIGHT + "            LOAN APPROVAL PREDICTION")
            print(Fore.CYAN + "=" * 50 + "\n")

            # Get user input with default values
            print(Fore.YELLOW + "Please provide the following details (press Enter to use default values):\n")
            gender = input(Fore.CYAN + "Gender (1=Male, 0=Female) [default=1]: ").strip()
            gender = int(gender) if gender else 1

            married = input(Fore.CYAN + "Married (1=Yes, 0=No) [default=1]: ").strip()
            married = int(married) if married else 1

            dependents = input(Fore.CYAN + "Number of Dependents [default=0]: ").strip()
            dependents = int(dependents) if dependents else 0

            education = input(Fore.CYAN + "Education (0=Graduate, 1=Not Graduate) [default=0]: ").strip()
            education = int(education) if education else 0

            self_employed = input(Fore.CYAN + "Self-Employed (1=Yes, 0=No) [default=0]: ").strip()
            self_employed = int(self_employed) if self_employed else 0

            applicant_income = input(Fore.CYAN + "Applicant Income [default=5000]: ").strip()
            applicant_income = float(applicant_income) if applicant_income else 5000.0

            coapplicant_income = input(Fore.CYAN + "Coapplicant Income [default=0]: ").strip()
            coapplicant_income = float(coapplicant_income) if coapplicant_income else 0.0

            loan_amount = input(Fore.CYAN + "Loan Amount [default=100]: ").strip()
            loan_amount = float(loan_amount) if loan_amount else 100.0

            loan_term = input(Fore.CYAN + "Loan Amount Term (in days) [default=360]: ").strip()
            loan_term = float(loan_term) if loan_term else 360.0

            credit_history = input(Fore.CYAN + "Credit History (1=Good, 0=Bad) [default=1]: ").strip()
            credit_history = int(credit_history) if credit_history else 1

            property_area = input(Fore.CYAN + "Property Area (0=Rural, 1=Semiurban, 2=Urban) [default=2]: ").strip()
            property_area = int(property_area) if property_area else 2

            # Simulate processing
            display_processing()

            # Create raw input data as a DataFrame
            input_data = pd.DataFrame({
                'Gender': ['Male' if gender == 1 else 'Female'],
                'Married': ['Yes' if married == 1 else 'No'],
                'Dependents': [str(dependents) if dependents < 3 else '3+'],
                'Education': ['Not Graduate' if education == 1 else 'Graduate'],
                'Self_Employed': ['Yes' if self_employed == 1 else 'No'],
                'ApplicantIncome': [applicant_income],
                'CoapplicantIncome': [coapplicant_income],
                'LoanAmount': [loan_amount],
                'Loan_Amount_Term': [loan_term],
                'Credit_History': [credit_history],
                'Property_Area': ['Rural' if property_area == 0 else 'Semiurban' if property_area == 1 else 'Urban']
            })

            # Perform one-hot encoding
            input_data = pd.get_dummies(input_data)

            # Ensure all expected features are present
            for feature in expected_features:
                if feature not in input_data.columns:
                    input_data[feature] = 0

            # Reorder columns to match the model's expected order
            input_data = input_data[expected_features]

            # Make a prediction
            prediction = model.predict(input_data)
            result = 'Approved' if prediction[0] == 1 else 'Rejected'

            # Display the result
            print(Fore.CYAN + "=" * 50)
            print(Fore.MAGENTA + Style.BRIGHT + f"Loan Approval Prediction: {Fore.GREEN + result}" if prediction[0] == 1 else f"Loan Approval Prediction: {Fore.RED + result}")
            print(Fore.CYAN + "=" * 50 + "\n")

            # Log the prediction
            with open('../data/prediction_log.txt', 'a') as log_file:
                log_file.write(f"Input: {input_data.to_dict(orient='records')}, Prediction: {result}\n")

        except ValueError:
            print(Fore.RED + "\nInvalid input. Please enter the correct data types for each field.\n")
        except KeyError as e:
            print(Fore.RED + f"\nError: Missing feature in input data - {str(e)}.\n")
        except Exception as e:
            print(Fore.RED + f"\nAn unexpected error occurred: {str(e)}\n")

        # Ask user if they want to continue
        user_choice = input(Fore.YELLOW + "Do you want to make another prediction? (yes/no): ").strip().lower()
        if user_choice == 'no':
            print(Fore.CYAN + "\nThank you for using the Loan Prediction System. Goodbye!")
            break

# Directly call the function
predict_loan()