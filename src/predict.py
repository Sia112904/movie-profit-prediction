import joblib
import pandas as pd

from src.preprocess import clean_movies
from src.features import build_features

# ---------------------------
# Load trained model + columns
# ---------------------------
MODEL_PATH = "data/models/best_model.pkl"
FEATURES_PATH = "data/results/feature_columns.pkl"

model = joblib.load(MODEL_PATH)
feature_columns = joblib.load(FEATURES_PATH)

print("Model and feature columns loaded.")

# ---------------------------
# Prediction function
# ---------------------------
def predict_profit(df):
    """
    Takes a raw movies dataframe and returns predicted profit.
    """

    # Clean and engineer features
    df = clean_movies(df)
    X = build_features(df)

    # Ensure column alignment
    X = X.reindex(columns=feature_columns, fill_value=0)

    # Predict
    predictions = model.predict(X)

    return predictions


# ---------------------------
# Run on new data
# ---------------------------
if __name__ == "__main__":

    # Load new movies
    new_movies = pd.read_csv("data/processed/new_movies.csv")

    # Generate predictions
    preds = predict_profit(new_movies)

    # Save results
    new_movies["predicted_profit"] = preds
    new_movies.to_csv("data/results/predicted_profits.csv", index=False)

    print("Predictions saved to data/results/predicted_profits.csv")

