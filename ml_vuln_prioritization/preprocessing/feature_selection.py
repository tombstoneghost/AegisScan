"""
Feature Selection
"""
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# Dataset
DATASET_PATH = "../data/cleaned_exploits_data.csv"

data = pd.read_csv(DATASET_PATH)


# Select relevant features
features = ['description', 'platform_code', 'type_code', 'author_code', 'date_published']

# Create a new DataFrame with selected features
data_selected = data[features]

# Check the selected features
print(data_selected.head())

# Initialize the TF-IDF vectorizer
tfidf = TfidfVectorizer(max_features=500)  # Limiting to 500 features to keep things manageable

# Transform the 'description' column into TF-IDF features
description_tfidf = tfidf.fit_transform(data_selected['description'])

# Convert the TF-IDF matrix to a DataFrame
description_df = pd.DataFrame(description_tfidf.toarray(), columns=tfidf.get_feature_names_out())

# Drop the original 'description' column from the dataset
data_selected = data_selected.drop(columns=['description'])

# Concatenate the TF-IDF DataFrame with the original data
data_selected = pd.concat([data_selected.reset_index(drop=True), description_df.reset_index(drop=True)], axis=1)


# Convert 'date_published' to datetime format and extract year (or other relevant components)
data_selected['date_published'] = pd.to_datetime(data_selected['date_published'])

# Extract year
data_selected['year_published'] = data_selected['date_published'].dt.year

# Drop the original 'date_published' column
data_selected = data_selected.drop(columns=['date_published'])

# Display the updated DataFrame
print("Updated Data Frame")
print(data_selected.head())

# Saving the data
data_selected.to_csv("../data/cleaned_vulnerability_data.csv")
