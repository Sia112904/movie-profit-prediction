import os
import numpy as np
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import MultiLabelBinarizer

from src.data_loader import load_movies
from src.preprocess import clean_movies

# ---------------------------
# Evaluation helper
# ---------------------------
def evaluate_model(model, X_test, y_test):
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2 = r2_score(y_test, preds)

    print(f"MAE : {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R²  : {r2:.3f}")

    return mae, rmse, r2

# ---------------------------
# Feature builder using saved MultiLabelBinarizer
# ---------------------------
def build_features_with_saved_mlb(df, mlb):
    features = pd.DataFrame()
    # Numeric features
    features["budget"] = df["budget"].fillna(0)
    features["runtime"] = df["runtime"].fillna(df["runtime"].median())
    features["release_year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year.fillna(0)
    # Genres
    genre_lists = df["genres"].apply(lambda x: [g["name"] for g in x] if isinstance(x, list) else [])
    genre_encoded = mlb.transform(genre_lists)
    genre_df = pd.DataFrame(genre_encoded, columns=mlb.classes_, index=df.index)
    features = pd.concat([features, genre_df], axis=1)
    return features

# ---------------------------
# Main training function
# ---------------------------
def main():
    # Load and clean data
    df = load_movies("data/processed/cleaned_movies.csv")
    df = clean_movies(df)
    df["profit"] = df["revenue"] - df["budget"]
    y = df["profit"]

    # ---------------------------
    # Fit MultiLabelBinarizer for genres and save
    # ---------------------------
    mlb = MultiLabelBinarizer()
    mlb.fit([ [g["name"] for g in x] if isinstance(x, list) else [] for x in df["genres"] ])
    os.makedirs("data/models", exist_ok=True)
    joblib.dump(mlb, "data/models/genre_mlb.pkl")
    print("Saved MultiLabelBinarizer for genres.")

    # ---------------------------
    # Build numeric features using saved MLB
    # ---------------------------
    X = build_features_with_saved_mlb(df, mlb)

    # Save feature columns (used later in evaluation)
    os.makedirs("data/results", exist_ok=True)
    joblib.dump(X.columns.tolist(), "data/results/feature_columns.pkl")
    print("Feature columns saved.")

    # ---------------------------
    # Train/test split
    # ---------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # ---------------------------
    # Random Forest
    # ---------------------------
    rf = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    print("\nRandom Forest Performance:")
    evaluate_model(rf, X_test, y_test)

    # ---------------------------
    # Gradient Boosting (BEST MODEL)
    # ---------------------------
    gbr = GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=3,
        random_state=42
    )
    gbr.fit(X_train, y_train)
    print("\nGradient Boosting Performance:")
    evaluate_model(gbr, X_test, y_test)

    # ---------------------------
    # Save BEST model
    # ---------------------------
    joblib.dump(gbr, "data/models/best_model.pkl")
    print("\nBest model saved to data/models/best_model.pkl")

if __name__ == "__main__":
    main()

