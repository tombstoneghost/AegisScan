"""
Pre-processing for dataset
"""
import pandas as pd

# Dataset
DATASET_PATH = "../data/files_exploits.csv"

data = pd.read_csv(DATASET_PATH)

print("Data Head")
print(data.head())

print("Data Info")
print(data.info())

print("Missing values")
print(data.isnull().sum())

print("Cleaning Data")

print("Dropping unnecessary columns")
# Drop columns with many missing values
data_cleaned = data.drop(columns=['port', 'tags', 'aliases', 'screenshot_url', 'application_url', 'source_url'])

# Fill missing date_updated with a placeholder or forward fill
data_cleaned['date_updated'].fillna('unknown', inplace=True)

# Fill missing codes with 'unknown'
data_cleaned['codes'].fillna('unknown', inplace=True)

# Convert date columns to datetime
data_cleaned['date_published'] = pd.to_datetime(data_cleaned['date_published'], errors='coerce')
data_cleaned['date_added'] = pd.to_datetime(data_cleaned['date_added'], errors='coerce')
data_cleaned['date_updated'] = pd.to_datetime(data_cleaned['date_updated'], errors='coerce')

# Convert categorical columns to category type
data_cleaned['platform'] = data_cleaned['platform'].astype('category')
data_cleaned['type'] = data_cleaned['type'].astype('category')
data_cleaned['author'] = data_cleaned['author'].astype('category')

# Create label encodings for categorical columns
data_cleaned['platform_code'] = data_cleaned['platform'].cat.codes
data_cleaned['type_code'] = data_cleaned['type'].cat.codes
data_cleaned['author_code'] = data_cleaned['author'].cat.codes

# Fill missing date_updated with corresponding date_added
data_cleaned['date_updated'].fillna(data_cleaned['date_added'], inplace=True)

# Drop original categorical columns after encoding
data_cleaned = data_cleaned.drop(columns=['platform', 'type', 'author'])

print("Missing values")
print(data_cleaned.isnull().sum())

# Save the cleaned data to a new CSV file
CLEANED_DATA_FILE = '../data/cleaned_exploits_data.csv'
data_cleaned.to_csv(CLEANED_DATA_FILE, index=False)

print(f"Cleaned data saved to {CLEANED_DATA_FILE}")
