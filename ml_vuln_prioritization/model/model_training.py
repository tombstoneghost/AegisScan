import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report

# Step 1: Load the preprocessed data from the CSV
df = pd.read_csv('../data/classified_exploits.csv')

# Feature selection
X = df[['description', 'platform_code', 'type_code', 'author_code', 'application_type']]
y = df['priority']

# Convert non-string columns to strings
X.columns = X.columns.astype(str)

# Handle missing or unknown 'application_type' values
X.loc[:, 'application_type'] = X['application_type'].fillna('Unknown')

# Apply one-hot encoding for the 'application_type' column
X = pd.get_dummies(X, columns=['application_type'])

# Apply TF-IDF to the 'description' column
vectorizer = TfidfVectorizer(max_features=1000)  # Limit to 1000 features
X_description = vectorizer.fit_transform(X['description']).toarray()

# Drop the 'description' column and concatenate the TF-IDF matrix
X = X.drop('description', axis=1)
X = pd.concat([X.reset_index(drop=True), pd.DataFrame(X_description)], axis=1)

# Ensure all columns are strings
X.columns = X.columns.astype(str)

pd.DataFrame(X).columns.to_series().to_csv('training_features.csv', index=False)

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize the RandomForestClassifier
clf = RandomForestClassifier()

# Train the model
clf.fit(X_train, y_train)

# Make predictions
y_pred = clf.predict(X_test)

# Evaluate the model
print(classification_report(y_test, y_pred))

# Save the trained model and the vectorizer
joblib.dump(clf, 'vulnerability_classification_model.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')

print("Model and vectorizer saved.")