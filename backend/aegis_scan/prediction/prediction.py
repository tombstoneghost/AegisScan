# Imports
import pandas as pd
import joblib

# Load the model
model = joblib.load('./aegis_scan/prediction/vulnerability_classification_model.pkl')

def predict(alerts: list, application_type: str):
    """
    Get Priority for all the alerts
    """
    alerts_df = pd.DataFrame(alerts)
    alerts_df['application_type'] = application_type

    # Process Data
    X = pd.get_dummies(alerts_df[['description', 'application_type']], columns=['application_type'], dummy_na=True)

    # Handle missing columns in the model
    for col in set(model.feature_names_in_) - set(X.columns):
        X[col] = 0
    X = X[model.feature_names_in_]

    # Predict priorities and update alerts
    alerts_df['ai_priority'] = model.predict(X)
    updated_alerts = alerts_df.to_dict(orient='records')

    return updated_alerts
