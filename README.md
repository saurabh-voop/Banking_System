# BankAdvance - A Simple Banking System

## Overview
BankAdvance is a web-based banking system built using Python and Streamlit. It allows users to create and manage bank accounts, perform transactions (deposits and withdrawals), and view account details and transaction history in an interactive interface.

## Features
- Create a new bank account with a unique account number
- Deposit and withdraw funds from an account
- View account details and current balance
- Access transaction history for each account
- Delete an account when no longer needed
- List all active bank accounts in the system

## Technologies Used
- **Python** (Backend logic and data handling)
- **Streamlit** (Frontend user interface)
- **Pandas** (For data display and manipulation)
- **UUID** (For unique account number generation)
- **Datetime** (For transaction timestamps)

## Installation
### Prerequisites
Ensure you have Python installed on your system.

### Steps
1. Clone this repository or download the `bankadvance.py` file.
2. Install required dependencies by running:
   ```sh
   pip install streamlit pandas
   ```
3. Run the application with:
   ```sh
   streamlit run bankadvance.py
   ```
4. Open the provided URL in your web browser to access the application.

## Usage
### Creating an Account
1. Enter the account holder's name.
2. Set an initial balance.
3. Choose an account type (Savings or Checking).
4. Click the **Create Account** button to generate a unique account number.

### Managing an Account
1. Enter the account number to retrieve account details.
2. View the balance and transaction history.
3. Deposit or withdraw funds using the respective input fields.
4. Delete the account if needed.

### Viewing All Accounts
- Navigate to the **List All Accounts** tab to view all active accounts in a tabular format.

## Error Handling
- The system prevents deposits or withdrawals with non-numeric values.
- Withdrawals are not allowed if the balance is insufficient.
- Account creation fails if initial values are invalid.
- Transactions are recorded with timestamps for accuracy.

## Future Enhancements
- Implement user authentication.
- Add support for transferring funds between accounts.
- Include graphical reports for financial analysis.
- Integrate a database for persistent data storage.

## License
This project is licensed under the MIT License.

## Author
Developed by [Your Name]

