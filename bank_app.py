
import streamlit as st
import json
import random
import string
from pathlib import Path

DB_FILE = 'data.json'

# Load data
if Path(DB_FILE).exists():
    with open(DB_FILE) as f:
        data = json.load(f)
else:
    data = []

# Save data
def save():
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Generate account number
def generate_account():
    alpha = random.choices(string.ascii_uppercase, k=3)
    nums = random.choices(string.digits, k=3)
    symbols = random.choices("!@#$%^&*", k=1)
    acc = alpha + nums + symbols
    random.shuffle(acc)
    return ''.join(acc)

# Get user
def get_user(acc_no, pin):
    return next((u for u in data if u['account No.'] == acc_no and u['pin'] == pin), None)

# Streamlit UI
st.set_page_config("Python Bank App", layout="centered")
st.title("🏦 Rohit Bank App")

menu = st.sidebar.selectbox("Menu", [
    "Create Account", "Deposit", "Withdraw", "View Details", "Update Info", "Delete Account"
])

if menu == "Create Account":
    st.subheader("📝 Create New Account")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    email = st.text_input("Email")
    pin = st.text_input("4-digit PIN", type='password')
    
    if st.button("Create"):
        if age < 18 or len(pin) != 4 or not pin.isdigit():
            st.error("Invalid input. Age must be 18+, and PIN must be 4 digits.")
        else:
            acc_no = generate_account()
            data.append({
                "name": name,
                "age": age,
                "email": email,
                "pin": int(pin),
                "account No.": acc_no,
                "balance": 0
            })
            save()
            st.success(f"Account created! Your Account Number: {acc_no}")

elif menu == "Deposit":
    st.subheader("💰 Deposit Money")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type='password')
    amount = st.number_input("Amount", min_value=1)

    if st.button("Deposit"):
        user = get_user(acc, int(pin))
        if not user:
            st.error("User not found.")
        elif amount > 10000:
            st.error("Maximum deposit limit is ₹10,000")
        else:
            user['balance'] += amount
            save()
            st.success("Amount deposited successfully.")

elif menu == "Withdraw":
    st.subheader("💸 Withdraw Money")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type='password')
    amount = st.number_input("Amount", min_value=1)

    if st.button("Withdraw"):
        user = get_user(acc, int(pin))
        if not user:
            st.error("User not found.")
        elif user['balance'] < amount:
            st.error("Insufficient balance.")
        else:
            user['balance'] -= amount
            save()
            st.success("Amount withdrawn successfully.")

elif menu == "View Details":
    st.subheader("📄 View Account Details")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type='password')

    if st.button("View"):
        user = get_user(acc, int(pin))
        if user:
            st.json(user)
        else:
            st.error("User not found.")

elif menu == "Update Info":
    st.subheader("✏️ Update Account Info")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type='password')

    if st.button("Fetch Info"):
        user = get_user(acc, int(pin))
        if user:
            new_name = st.text_input("New Name", user['name'])
            new_email = st.text_input("New Email", user['email'])
            new_pin = st.text_input("New PIN", value=str(user['pin']), type='password')
            
            if st.button("Update"):
                user['name'] = new_name
                user['email'] = new_email
                if new_pin.isdigit() and len(new_pin) == 4:
                    user['pin'] = int(new_pin)
                    save()
                    st.success("Information updated.")
                else:
                    st.error("PIN must be 4 digits.")
        else:
            st.error("User not found.")

elif menu == "Delete Account":
    st.subheader("🗑️ Delete Account")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type='password')

    if st.button("Delete"):
        user = get_user(acc, int(pin))
        if user:
            data.remove(user)
            save()
            st.success("Account deleted.")
        else:
            st.error("User not found.")
