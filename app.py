import streamlit as st
import pandas as pd
import numpy as np

# Google Analytics integration
st.markdown(f'<script async src="https://www.googletagmanager.com/gtag/js?id=G-8NHG39VPS0"></script>', unsafe_allow_html=True)
st.markdown("""
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-8NHG39VPS0');
    </script>
""", unsafe_allow_html=True)

# CSS styles
st.markdown("""
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f7f7f7;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 300px;
            text-align: center;
        }
        .title {
            color: blue;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .subtitle {
            font-size: 12px;
            margin-bottom: 20px;
        }
        .input-group {
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }
        .icon {
            width: 20px;
            margin-right: 10px;
        }
        input[type="email"], input[type="password"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        .options {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
        }
        .remember-me {
            font-size: 14px;
        }
        .forgot-password {
            font-size: 14px;
            color: blue;
            text-decoration: none;
        }
        .sign-in-button {
            background-color: blue;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
        }
        .register-text {
            font-size: 12px;
            margin-top: 10px;
        }
        .signup-link {
            color: blue;
            font-weight: bold;
            text-decoration: none;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="container">', unsafe_allow_html=True)
st.markdown('<h1 class="title">SIGN IN</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Please enter your email and password</p>', unsafe_allow_html=True)

# Input Fields
email = st.text_input("Email Address", placeholder="Enter your email", key="email", help='Enter your email')
password = st.text_input("Password", placeholder="Enter your password", type="password", key="password", help='Enter your password')

# Session Management
if 'signed_in' not in st.session_state:
    st.session_state['signed_in'] = False

if st.session_state['signed_in']:
    st.success(f"Welcome back, {st.session_state['email']}!")

if not st.session_state['signed_in']:
    if st.button("Sign In"):
        # Save user data in session state
        st.session_state['signed_in'] = True
        st.session_state['email'] = email
        st.success("Signed In Successfully")

# Register Link
st.markdown('<p class="register-text">Don\'t have an account? <a href="#" class="signup-link">Sign Up Now</a></p>', unsafe_allow_html=True)

# Close the container div
st.markdown('</div>', unsafe_allow_html=True)

# Load data (modify as needed)
restaurant_data = pd.read_csv('restaurant_orders.csv')
tattoo_data = pd.read_csv('tattoo_shop_orders.csv')

# Enhance the Interface
st.title("Breeze Supply Sight")

# Dropdown for business selection
business_type = st.selectbox("Select Business Type", ["Restaurant", "Tattoo Shop"])

# Sliders for order filters
min_orders = st.slider("Minimum Orders", 0, 100, 10)
max_orders = st.slider("Maximum Orders", 0, 100, 50)

# File upload for custom data
uploaded_file = st.file_uploader("Upload your data file", type=["csv"])
if uploaded_file is not None:
    try:
        custom_data = pd.read_csv(uploaded_file)
        st.write(custom_data)
    except Exception as e:
        st.error("Error loading file. Please upload a valid CSV.")

# Budget Tracking
st.subheader("Budget Tracking")
budget_goal = st.number_input("Set your budget goal:", min_value=0.0, value=1000.0, step=100.0)
actual_spending = st.number_input("Enter your actual spending:", min_value=0.0, value=0.0, step=100.0)

# Check if actual spending exceeds budget
if actual_spending > budget_goal:
    st.warning("Warning: Actual spending exceeds the budget goal.")
else:
    st.success("Your spending is within the budget.")

# Budget vs. Actual Spending Visualization
st.subheader("Budget vs Actual Spending")
if budget_goal and actual_spending >= 0:
    budget_data = pd.DataFrame({
        'Category': ['Budget Goal', 'Actual Spending'],
        'Amount': [budget_goal, actual_spending]
    })
    st.bar_chart(budget_data.set_index('Category'))

# Supplier Management
st.subheader("Supplier Management")
supplier_name = st.text_input("Supplier Name")
contact_details = st.text_input("Contact Details")
delivery_time = st.number_input("Average Delivery Time (days)", min_value=1, value=3)
reliability_rating = st.selectbox("Reliability Rating", [1, 2, 3, 4, 5])

if st.button("Add Supplier"):
    st.success(f"Supplier '{supplier_name}' added with delivery time {delivery_time} days and reliability rating {reliability_rating}.")

# Display Suppliers
st.subheader("Supplier List")
if st.button("Show Suppliers"):
    supplier_data = pd.DataFrame({
        'Supplier Name': ['Supplier A', 'Supplier B'],
        'Contact Details': ['contactA@example.com', 'contactB@example.com'],
        'Delivery Time (days)': [2, 5],
        'Reliability Rating': [4, 3]
    })
    st.write(supplier_data)

# Supplier Recommendations based on reliability rating
if st.button("Recommend Supplier"):
    suppliers = {
        'Supplier A': {'rating': 4, 'delivery_time': 2},
        'Supplier B': {'rating': 3, 'delivery_time': 5}
    }
    best_supplier = max(suppliers, key=lambda k: suppliers[k]['rating'])
    st.success(f"Best supplier based on reliability: {best_supplier} with a rating of {suppliers[best_supplier]['rating']}.")

# Visualizations
st.subheader("Orders Histogram")
if business_type == "Restaurant":
    st.bar_chart(restaurant_data['orders'])
elif business_type == "Tattoo Shop":
    st.bar_chart(tattoo_data['orders'])

# AI-Powered Recommendations
st.subheader("AI-Powered Recommendations")
if st.button("Get Recommendations"):
    # Placeholder for recommendation logic
    if business_type == "Restaurant":
        recommended_stock = int(restaurant_data['orders'].mean() * 1.2)  # 20% more than average
        st.success(f"Recommended stock level for Restaurant: {recommended_stock} items.")
    elif business_type == "Tattoo Shop":
        recommended_stock = int(tattoo_data['orders'].mean() * 1.2)  # 20% more than average
        st.success(f"Recommended stock level for Tattoo Shop: {recommended_stock} items.")

# User feedback
st.subheader("User Feedback")
feedback = st.text_area("What do you think about the app?")
if st.button("Submit Feedback"):
    st.success("Thank you for your feedback!")

# User guide
st.subheader("User Guide")
st.write("""
- **Select Business Type**: Choose between Restaurant and Tattoo Shop to filter data.
- **Upload Data**: You can upload your own CSV files to analyze.
- **Adjust Parameters**: Use the sliders to filter data according to order quantity.
- **Set Budget**: Input your budget goal and actual spending to track your finances.
- **Manage Suppliers**: Add and view supplier information, including contact details and delivery times.
- **Get Recommendations**: Click to receive personalized stock level recommendations based on historical data.
""")

# GitHub Link
st.markdown("[View Source Code on GitHub](https://github.com/juanc/icwucn_projects)")

# Mobile Optimization
if st.checkbox("Mobile Optimization"):
    st.write("Optimized for mobile!")
    st.markdown("""
    <style>
        @media (max-width: 600px) {
            .container {
                width: 90%;
            }
        }
    </style>
    """, unsafe_allow_html=True)
