import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from prophet import Prophet
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from statsmodels.tsa.seasonal import seasonal_decompose

# Set page config
st.set_page_config(page_title="Breeze Supply Sight", layout="wide")

# Link to the CSS file
st.markdown('<link rel="stylesheet" href="styles.css">', unsafe_allow_html=True)

# Database setup (using SQLite for simplicity)
conn = sqlite3.connect('users.db')
c = conn.cursor()

def create_user_table():
    c.execute('CREATE TABLE IF NOT EXISTS users(email TEXT, password TEXT)')  # Change username to email
    conn.commit()

def add_user(email, password):
    c.execute('INSERT INTO users(email, password) VALUES (?, ?)', (email, password))
    conn.commit()

def login_user(email, password):
    c.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    data = c.fetchall()
    return data

# Check user session state for login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Page 1: Login
if not st.session_state.logged_in:
    st.title("Welcome to Breeze Supply Sight")
    
    # User Login
    st.subheader("Login to Your Account")
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    
    if st.button("Log In", key="login_button"):  # Unique key added here
        result = login_user(email, password)
        if result:
            st.success(f"Welcome, {email}!")
            st.session_state.logged_in = True
        else:
            st.warning("Incorrect Email/Password")

    st.markdown("<small><a href='#'>Forgotten your password?</a></small>", unsafe_allow_html=True)
    st.markdown("<small>Don't have an account?</small>", unsafe_allow_html=True)

    if st.button("Create Account", key="create_account_nav"):  # Unique key added here
        st.session_state.create_account = True  # Navigate to Create Account page

# Page 2: Create Account
if 'create_account' in st.session_state and st.session_state.create_account:
    st.title("Create New Account")
    
    first_name = st.text_input("First Name", placeholder="Enter your first name", key="first_name")
    last_name = st.text_input("Last Name", placeholder="Enter your last name", key="last_name")
    email = st.text_input("Email", placeholder="Enter your email", key="email")  # Changed to email
    new_password = st.text_input("Password", type="password", placeholder="Enter your password", key="new_password")
    
    if st.button("Create Account", key="create_account_button"):  # Unique key added here
        create_user_table()
        add_user(email, new_password)  # Save email instead of username
        st.success("You have successfully created an account!")
        st.info("You can now log in with your credentials.")
        st.session_state.create_account = False  # Reset to go back to the login page

# Page 3: Main Menu
if st.session_state.logged_in:
    # Sidebar Menu
    selected = st.sidebar.selectbox("Main Menu", ["Home", "Profile", "Budget Tracking", "Custom Events", "AI Prediction"])
    
    # Home Page - Supply Prediction and Management
    if selected == "Home":
        st.title("Breeze Supply Sight")
        st.subheader("Supply Prediction Dashboard")

        # Load data
        uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
        
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write("Preview of Data:", df.head())
            
            # Ensure the necessary columns exist
            if 'date' in df.columns and 'expenses' in df.columns:
                df['ds'] = pd.to_datetime(df['date'])
                df['y'] = df['expenses']

                # Feature Engineering - Creating Lag Features
                for lag in range(1, 4):  # Creates lag_1, lag_2, lag_3
                    df[f'lag_{lag}'] = df['y'].shift(lag)
                st.write("Data with Lag Features:", df.head())

                # Seasonal Decomposition
                df.set_index('ds', inplace=True)
                decomposition = seasonal_decompose(df['y'], model='additive', period=30)
                fig_decompose = decomposition.plot()
                plt.suptitle("Seasonal Decomposition")
                st.pyplot(fig_decompose)

                # Time Series Forecasting using Facebook Prophet
                model = Prophet()
                model.fit(df[['ds', 'y']])
                
                future = model.make_future_dataframe(periods=365)
                forecast = model.predict(future)
                
                st.write("Supply Prediction for Next Year:")
                fig1 = model.plot(forecast)
                st.pyplot(fig1)
            
                # Additional Data Visualizations
                st.subheader("Data Visualizations")
                fig2 = px.line(df.reset_index(), x='ds', y='y', title='Expenses Over Time')
                st.plotly_chart(fig2)

                # Model retraining mechanism
                if st.button("Retrain Model"):
                    model.fit(df[['ds', 'y']])
                    st.success("Model retrained with the new data!")

    # User Profile
    if selected == "Profile":
        st.subheader("User Profile")
        st.write("Welcome to your profile page.")

    # Budget Tracking
    if selected == "Budget Tracking":
        st.subheader("Budget Tracking")
        
        budget = st.number_input("Enter your monthly budget", min_value=0.0)
        expense = st.number_input("Enter an expense amount", min_value=0.0)
        
        # Store expenses in a session state
        if 'expenses' not in st.session_state:
            st.session_state.expenses = []
        
        if st.button("Add Expense"):
            st.session_state.expenses.append(expense)
            st.success(f"Added expense: ${expense:.2f}")
        
        total_expenses = sum(st.session_state.expenses)
        st.write(f"Total Expenses: ${total_expenses:.2f}")

        if total_expenses > budget:
            st.warning(f"You have exceeded your budget! Total Expenses: ${total_expenses:.2f}")
        else:
            st.success(f"Total Expenses: ${total_expenses:.2f}, within budget.")

    # Custom Event Inputs
    if selected == "Custom Events":
        st.subheader("Log Custom Events")
        
        event_name = st.text_input("Event Name", placeholder="Enter event name")
        event_date = st.date_input("Event Date")
        event_description = st.text_area("Event Description", placeholder="Describe the event")
        
        if st.button("Log Event"):
            st.success(f"Logged event: {event_name} on {event_date}")

    # AI Prediction
    if selected == "AI Prediction":
        st.subheader("Expense Prediction using Machine Learning")
        
        # Load and prepare the data for ML
        if uploaded_file is not None:
            df_ml = pd.read_csv(uploaded_file)
            
            # Ensure the necessary columns exist
            if 'date' in df_ml.columns and 'expenses' in df_ml.columns:
                df_ml['ds'] = pd.to_datetime(df_ml['date'])
                df_ml['y'] = df_ml['expenses']
                
                # Create features for the model
                df_ml['month'] = df_ml['ds'].dt.month
                df_ml['day'] = df_ml['ds'].dt.day
                df_ml['year'] = df_ml['ds'].dt.year
                
                # Create Lag Features
                for lag in range(1, 4):  # Creates lag_1, lag_2, lag_3
                    df_ml[f'lag_{lag}'] = df_ml['y'].shift(lag)
                
                X = df_ml[['month', 'day', 'year', 'lag_1', 'lag_2', 'lag_3']].dropna()
                y = df_ml['y'][X.index]
                
                # Split the data into training and testing sets
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                
                # Train a linear regression model
                regressor = LinearRegression()
                regressor.fit(X_train, y_train)
                
                # Make predictions
                predictions = regressor.predict(X_test)
                
                # Evaluate model performance
                mae = mean_absolute_error(y_test, predictions)
                r2 = r2_score(y_test, predictions)
                
                # Show predictions and performance metrics
                st.write("Predictions on Test Data:")
                pred_df = pd.DataFrame({'Actual': y_test, 'Predicted': predictions})
                st.write(pred_df)
                st.write(f"Mean Absolute Error: {mae:.2f}")
                st.write(f"R-squared: {r2:.2f}")
