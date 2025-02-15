import streamlit as st
import uuid
import datetime
import pandas as pd


class BankAccount:
    """
    Represents a single bank account.
    """

    def __init__(
        self, account_holder_name, initial_balance=0.0, account_type="Savings"
    ):
        if not isinstance(initial_balance, (int, float)):
            raise TypeError("Initial balance must be a number.")
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")

        self.account_number = str(uuid.uuid4())
        self.account_holder_name = account_holder_name
        self.balance = initial_balance
        self.account_type = account_type
        self.transactions = []
        self.creation_date = datetime.date.today()

    def deposit(self, amount):
        if not isinstance(amount, (int, float)):
            raise TypeError("Deposit amount must be a number.")
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")

        self.balance += amount
        self._add_transaction("Deposit", amount)

    def withdraw(self, amount):
        if not isinstance(amount, (int, float)):
            raise TypeError("Withdrawal amount must be a number.")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")

        self.balance -= amount
        self._add_transaction("Withdrawal", -amount)

    def get_balance(self):
        return self.balance

    def get_account_details(self):
        details = {
            "Account Number": self.account_number,
            "Account Holder": self.account_holder_name,
            "Account Type": self.account_type,
            "Balance": self.balance,
            "Creation Date": self.creation_date,
        }
        return details

    def _add_transaction(self, transaction_type, amount):
        timestamp = datetime.datetime.now()
        self.transactions.append(
            {"timestamp": timestamp, "type": transaction_type, "amount": amount}
        )

    def get_transaction_history(self):
        return self.transactions


class BankingSystem:
    def __init__(self):
        self.accounts = {}

    def create_account(
        self, account_holder_name, initial_balance=0.0, account_type="Savings"
    ):
        try:
            account = BankAccount(account_holder_name, initial_balance, account_type)
            self.accounts[account.account_number] = account
            return account.account_number
        except (TypeError, ValueError) as e:
            return None

    def get_account(self, account_number):
        return self.accounts.get(account_number)

    def delete_account(self, account_number):
        if account_number in self.accounts:
            del self.accounts[account_number]
            return "Account deleted successfully."
        else:
            return "Account not found."

    def list_all_accounts(self):
        account_data = []
        for acc_num, acc in self.accounts.items():
            account_data.append(acc.get_account_details())
        return account_data


if "bank" not in st.session_state:
    st.session_state.bank = BankingSystem()

st.title("My Bank")

tab1, tab2, tab3 = st.tabs(["Create Account", "Manage Account", "List All Accounts"])

with tab1:
    st.header("Create New Account")
    name = st.text_input("Account Holder Name")
    initial_balance = st.number_input("Initial Balance", min_value=0.0, format="%.2f")
    account_type = st.selectbox("Account Type", ["Savings", "Checking"])

    if st.button("Create Account"):
        if name:
            account_number = st.session_state.bank.create_account(
                name, initial_balance, account_type
            )
            if account_number:
                st.success(
                    f"Account created successfully! Account Number: {account_number}"
                )
            else:
                st.error("Account creation failed. Please check the input values.")
        else:
            st.warning("Please enter an account holder name.")

with tab2:
    st.header("Manage Existing Account")
    account_number = st.text_input("Enter Account Number", key="manage_account_number")
    account = st.session_state.bank.get_account(account_number)

    if account:
        st.subheader("Account Details")
        details = account.get_account_details()
        for key, value in details.items():
            st.write(f"{key}: {value if key != 'Balance' else f'${value:.2f}'}")

        st.subheader("Transactions")
        transaction_type = st.selectbox("Transaction Type", ["Deposit", "Withdraw"])
        amount = st.number_input(
            "Amount", min_value=0.0, format="%.2f", key="transaction_amount"
        )

        if st.button(transaction_type):
            try:
                if transaction_type == "Deposit":
                    account.deposit(amount)
                    st.success(
                        f"Deposited ${amount:.2f}. New balance: ${account.get_balance():.2f}"
                    )
                elif transaction_type == "Withdraw":
                    account.withdraw(amount)
                    st.success(
                        f"Withdrew ${amount:.2f}. New balance: ${account.get_balance():.2f}"
                    )
            except (TypeError, ValueError) as e:
                st.error(str(e))

        st.subheader("Transaction History")
        transactions = account.get_transaction_history()
        if transactions:
            df = pd.DataFrame(transactions)
            df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
            df["amount"] = df["amount"].apply(lambda x: f"${x:.2f}")
            st.dataframe(df)
        else:
            st.write("No transactions yet.")

        st.subheader("Delete Account")
        if st.button("Delete Account", type="primary"):
            result = st.session_state.bank.delete_account(account.account_number)
            st.success(result)
            st.session_state.manage_account_number = ""
            st.rerun()

    elif account_number:
        st.error("Account not found.")


with tab3:
    st.header("List of All Accounts")
    accounts_data = st.session_state.bank.list_all_accounts()
    if accounts_data:
        df = pd.DataFrame(accounts_data)
        df["Balance"] = df["Balance"].apply(lambda x: f"${x:.2f}")
        st.dataframe(df)
    else:
        st.write("No accounts in the system.")