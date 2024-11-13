import pandas as pd
import joblib

# Load the model
model = joblib.load('vulnerability_classification_model.pkl')

# Prepare the new data for prediction
data = [
    {
        "description": "Server Leaks Version Information via \"Server\" HTTP Response Header Field",
        "application_type": "blog"
    },
    {
        "description": "WPanel 4.3.1 - Remote Code Execution (RCE) (Authenticated) ",
        "application_type": "blog"
    }
]

# Create a DataFrame
X_new = pd.DataFrame(data)

# Fill missing values if necessary
X_new['application_type'] = X_new['application_type'].fillna('Unknown')

# One-hot encode the application_type column
X_new = pd.get_dummies(X_new, columns=['application_type'])

# Ensure that the columns match the model's training data
missing_cols = set(model.feature_names_in_) - set(X_new.columns)
for col in missing_cols:
    X_new[col] = 0

X_new = X_new[model.feature_names_in_]

# Make predictions
predictions = model.predict(X_new)

# Output the predictions
print(predictions)
