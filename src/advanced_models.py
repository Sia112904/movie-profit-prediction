import numpy as np
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from src.data_loader import load_movies
from src.preprocess import clean_movies
from src.features import build_features

def evaluate_model(model, X_test, y_test):
    """Evaluate model performance and print metrics."""
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2 = r2_score(y_test, preds)

    print("MAE:", mae)
    print("RMSE:", rmse)
    print("R²:", r2)

    return mae, rmse, r2


def main():
    # ----------------------
    # Load and clean data
    # ----------------------
    try:
        df = load_movies("data/processed/cleaned_movies.csv")
    except FileNotFoundError:
        print("Error: cleaned_movies.csv not found in data/processed/")
        return

    df = clean_movies(df)

    # ----------------------
    # Ensure target column exists
    # ----------------------
    if "profit" not in df.columns:
        if "revenue" in df.columns and "budget" in df.columns:
            df["profit"] = df["revenue"] - df["budget"]
            print("Created 'profit' column as revenue - budget")
        else:
            raise ValueError("Cannot create 'profit': missing 'revenue' or 'budget' columns")

    # ----------------------
    # Define target and features
    # ----------------------
    y = df["profit"]
    X = build_features(df)

    # Save feature columns for later prediction
    import joblib
    joblib.dump(X.columns.tolist(), "data/results/feature_columns.pkl")


    print("Feature columns:", X.columns.tolist())
    print("Target column head:\n", y.head())

    # ----------------------
    # Train-test split
    # ----------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    # ----------------------
    # Random Forest Regressor
    # ----------------------
    rf = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )
    rf.fit(X_train, y_train)
    print("\nRandom Forest (baseline)")
    evaluate_model(rf, X_test, y_test)

    # Save model
    joblib.dump(rf, "data/results/rf_model.pkl")
    print("Random Forest model saved to data/results/rf_model.pkl")

    # ----------------------
    # Gradient Boosting Regressor
    # ----------------------
    gbr = GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=3,
        random_state=42
    )
    gbr.fit(X_train, y_train)
    print("\nGradient Boosting")
    evaluate_model(gbr, X_test, y_test)

    # Save model
    joblib.dump(gbr, "data/results/gbr_model.pkl")
    print("Gradient Boosting model saved to data/results/gbr_model.pkl")


if __name__ == "__main__":
    main()

