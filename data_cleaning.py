import pandas as pd
import glob
import os

# Specify the directory containing your CSV files
directory = r'C:\Users\juanc\OneDrive\Documents\icwucn_projects\icwucn2025k'

# Use glob to get all CSV files in the directory
file_paths = glob.glob(os.path.join(directory, '*.csv'))

# Loop through each file, load and clean
for file_path in file_paths:
    try:
        # Load the data using pandas
        data = pd.read_csv(file_path)

        # Check for missing values
        missing_values = data.isnull().sum()
        print(f"Missing values in {file_path}:")
        print(missing_values)

        # Remove missing values
        cleaned_data = data.dropna()
        print(f"\nData after removing missing values from {file_path}:")
        print(cleaned_data)

        # Save the cleaned data to a new file
        cleaned_file_path = file_path.replace('.csv', '_cleaned.csv')
        cleaned_data.to_csv(cleaned_file_path, index=False)
        print(f"Cleaned data saved to {cleaned_file_path}\n")

    except Exception as e:
        print(f"An error occurred while processing {file_path}: {str(e)}")
