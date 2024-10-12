import quandl
import pandas as pd

# Set your API key
quandl.ApiConfig.api_key = "395c65eaeb7c2670629648a34493c823"

# Fetching a dataset
try:
    # Example: Fetching Apple Inc. stock data
    data = quandl.get("WIKI/AAPL")  # Replace with the dataset you want to access
    print("Data fetched successfully:")
    print(data.head())  # Print the first few rows of the dataset

    # Save data to a CSV file
    data.to_csv('apple_stock_data.csv')  # Save the data for later use
    print("Data saved to apple_stock_data.csv")

except Exception as e:
    print(f"An error occurred: {e}")
