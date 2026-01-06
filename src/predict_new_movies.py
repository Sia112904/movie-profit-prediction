# src/predict_new_movies.py
import pandas as pd
import joblib
import os

from src.preprocess import clean_movies
from src.features import build_features

def align_features(X_new, X_train_columns):
    """
    Make sure X_new has all columns that X_train had during training.
    Missing columns are added with zeros (all at once to avoid fragmentation),
    extra columns removed, and columns are ordered to match training.
    """
    # Identify missing columns
    missing_cols = [col for col in X_train_columns if col not in X_new.columns]
    
    # Add all missing columns at once
    if missing_cols:
        X_new = pd.concat([X_new, pd.DataFrame(0, index=X_new.index, columns=missing_cols)], axis=1)
    
    # Reorder columns to match training
    X_new = X_new[X_train_columns]
    
    return X_new


def main():
    # ----------------------
    # Paths
    # ----------------------
    new_movies_path = "data/processed/new_movies.csv"
    model_path = "data/results/rf_model.pkl"
    feature_columns_path = "data/results/feature_columns.pkl"
    output_path = "data/results/predicted_profits.csv"

    # ----------------------
    # Check required files exist
    # ----------------------
    for path in [new_movies_path, model_path, feature_columns_path]:
        if not os.path.exists(path):
            print(f"Error: {path} not found")
            return

    # ----------------------
    # Load new movies CSV
    # ----------------------
    new_movies = pd.read_csv(new_movies_path, on_bad_lines="skip")
    new_movies = clean_movies(new_movies)
    X_new = build_features(new_movies)

    # ----------------------
    # Load trained model
    # ----------------------
    rf = joblib.load(model_path)

    # ----------------------
    # Load training feature columns and align
    # ----------------------
    feature_columns = joblib.load(feature_columns_path)
    X_new = align_features(X_new, feature_columns)

    # ----------------------
    # Predict profits
    # ----------------------
    predicted_profits = rf.predict(X_new)

    # ----------------------
    # Save predictions
    # ----------------------
    movie_ids = new_movies["id"] if "id" in new_movies.columns else new_movies.index
    pred_df = pd.DataFrame({
        "movie_id": movie_ids,
        "predicted_profit": predicted_profits
    })

    pred_df.to_csv(output_path, index=False)
    print(f"Predictions saved to {output_path}")
    print(pred_df.head())

if __name__ == "__main__":
    main()

