import streamlit as st
import sqlite3
from datetime import datetime

# Set page config
st.set_page_config(page_title="Breeze Supply Sight", layout="wide")

# Database setup (using SQLite for simplicity)
conn = sqlite3.connect('users.db')
c = conn.cursor()

def create_user_table():
    c.execute('CREATE TABLE IF NOT EXISTS users(email TEXT PRIMARY KEY, password TEXT)')
    conn.commit()

def add_user(email, password):
    try:
        c.execute('INSERT INTO users(email, password) VALUES (?, ?)', (email, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(email, password):
    c.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    return c.fetchall()

def create_supply_table():
    c.execute('CREATE TABLE IF NOT EXISTS supply_items( \
        id INTEGER PRIMARY KEY AUTOINCREMENT, \
        email TEXT, \
        name TEXT, \
        order_date TEXT, \
        price REAL, \
        quantity INTEGER, \
        location TEXT)')
    conn.commit()

def add_supply_item(email, name, order_date, price, quantity, location):
    c.execute('INSERT INTO supply_items(email, name, order_date, price, quantity, location) VALUES (?, ?, ?, ?, ?, ?)', 
              (email, name, order_date, price, quantity, location))
    conn.commit()

def get_supply_items(email):
    c.execute('SELECT * FROM supply_items WHERE email = ?', (email,))
    return c.fetchall()

def reset_supply_items(email):
    c.execute('DELETE FROM supply_items WHERE email = ?', (email,))
    conn.commit()

# Create the user and supply tables on app start
create_user_table()
create_supply_table()

# Check user session state for login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Page 1: Login
if not st.session_state.logged_in:
    st.title("Welcome to Breeze Supply Sight")
    st.markdown("<div style='position: absolute; top: 10px; right: 10px;'><span style='color: blue;'>BETA</span></div>", unsafe_allow_html=True)
    
    # User Login
    st.subheader("Login to Your Account")
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    
    remember_me = st.checkbox("Remember Me")

    if st.button("Log In", key="login_button"):
        result = login_user(email, password)
        if result:
            st.success(f"Welcome, {email}!")
            st.session_state.logged_in = True
            st.session_state.logged_in_email = email  # Initialize logged_in_email
            if remember_me:
                st.session_state.remember_me = True
        else:
            st.warning("Incorrect Email/Password. If you don't have an account, please create one or recover your password.")

    # 'Password Help?' and 'Create New Account' links
    st.markdown("<small><a href='#'>Forgotten your password?</a></small>", unsafe_allow_html=True)
    st.markdown("<small>Don't have an account?</small>", unsafe_allow_html=True)
    if st.button("Create New Account", key="create_account_nav"):
        st.session_state.create_account = True

# Page 2: Create Account
if 'create_account' in st.session_state and st.session_state.create_account:
    st.title("Create New Account")
    
    first_name = st.text_input("First Name", placeholder="Enter your first name", key="first_name")
    last_name = st.text_input("Last Name", placeholder="Enter your last name", key="last_name")
    email = st.text_input("Email", placeholder="Enter your email", key="email")
    new_password = st.text_input("Password", type="password", placeholder="Enter your password", key="new_password")
    
    if st.button("Create Account", key="create_account_button"):
        if add_user(email, new_password):
            st.success("You have successfully created an account!")
            st.info("You can now log in with your credentials.")
            st.session_state.create_account = False
        else:
            st.warning("An account with this email already exists. Please log in or recover your password.")

# Page 3: Main Menu
if st.session_state.logged_in:
    # Sidebar Menu
    selected = st.sidebar.selectbox("Main Menu", ["Home", "Profile", "Budget Tracking", "Custom Events", "AI Prediction"])
    
    # Add Logout Button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.logged_in_email = ""  # Clear the stored email
        st.session_state.create_account = False  # Reset create_account state
        st.session_state.remember_me = False  # Reset remember_me state

    # Home Page - Supply Prediction and Management
    if selected == "Home":
        st.title("Breeze Supply Sight")
        st.subheader("Supply Prediction Dashboard")

        # Input for new supply item
        with st.form(key='add_supply_item_form'):
            name = st.text_input("Item Name", placeholder="Enter item name")
            order_date = st.date_input("Order Date", value=datetime.now())
            price = st.number_input("Price", min_value=0.0, step=0.01, format="%.2f")
            quantity = st.number_input("Quantity", min_value=1, step=1)
            location = st.text_input("Location", placeholder="Enter item location")
            submit_button = st.form_submit_button("Add Supply Item")

            if submit_button:
                add_supply_item(st.session_state.logged_in_email, name, order_date, price, quantity, location)
                st.success(f"Added {name} to your supply list!")

        # Display supply items
        st.subheader("Your Supply Items")
        supply_items = get_supply_items(st.session_state.logged_in_email)
        
        if supply_items:
            for item in supply_items:
                st.markdown(f"**Item:** {item[2]}  |  **Order Date:** {item[3]}  |  **Price:** ${item[4]:.2f}  |  **Quantity:** {item[5]}  |  **Location:** {item[6]}")
        else:
            st.info("No supply items found. Add some above!")

        # Reset button to clear all supply items
        if st.button("Reset Supply Items"):
            reset_supply_items(st.session_state.logged_in_email)
            st.success("Your supply items have been reset!")

