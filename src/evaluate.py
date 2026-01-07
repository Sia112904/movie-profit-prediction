import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from src.data_loader import load_movies
from src.preprocess import clean_movies

# ---------------------------
# Feature builder using saved MultiLabelBinarizer
# ---------------------------
def build_features_with_saved_mlb(df, mlb):
    """
    Build numeric features for the model using the same MultiLabelBinarizer
    that was used during training.
    """
    features = pd.DataFrame()

    # Numeric columns
    features["budget"] = df["budget"].fillna(0)
    features["runtime"] = df["runtime"].fillna(df["runtime"].median())

    # Release year
    features["release_year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year.fillna(0)

    # Genres: use saved MultiLabelBinarizer
    if "genres" in df.columns:
        genre_lists = df["genres"].apply(lambda x: [g["name"] for g in x] if isinstance(x, list) else [])
        genre_encoded = mlb.transform(genre_lists)
        genre_df = pd.DataFrame(genre_encoded, columns=mlb.classes_, index=df.index)
        features = pd.concat([features, genre_df], axis=1)

    return features

# ---------------------------
# Load processed dataset
# ---------------------------
df = load_movies("data/processed/cleaned_movies.csv")
df = clean_movies(df)
df["profit"] = df["revenue"] - df["budget"]

# ---------------------------
# Load trained model and saved MultiLabelBinarizer
# ---------------------------
model = joblib.load("data/models/best_model.pkl")
mlb = joblib.load("data/models/genre_mlb.pkl")  # This must be saved during training

# ---------------------------
# Build features using saved ML transformer
# ---------------------------
X = build_features_with_saved_mlb(df, mlb)
y = df["profit"]

# ---------------------------
# Train/test split
# ---------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------------------
# Align columns with model
# ---------------------------
X_train = X_train.reindex(columns=model.feature_names_in_, fill_value=0)
X_test = X_test.reindex(columns=model.feature_names_in_, fill_value=0)
feature_names = X_train.columns

# ---------------------------
# Predictions
# ---------------------------
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# ---------------------------
# Evaluation metrics
# ---------------------------
train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
train_r2 = r2_score(y_train, y_train_pred)
test_r2 = r2_score(y_test, y_test_pred)

print("MODEL PERFORMANCE")
print("------------------")
print(f"Train RMSE: {train_rmse:.2f}")
print(f"Test  RMSE: {test_rmse:.2f}")
print(f"Train R²  : {train_r2:.3f}")
print(f"Test  R²  : {test_r2:.3f}")

# ---------------------------
# Residual plot (TEST set)
# ---------------------------
residuals = y_test - y_test_pred
plt.figure()
plt.scatter(y_test_pred, residuals, alpha=0.5)
plt.axhline(0, color="red", linestyle="--")
plt.xlabel("Predicted Profit")
plt.ylabel("Residuals")
plt.title("Residual Plot (Test Set)")
plt.savefig("data/results/residual_plot.png")
plt.close()

# ---------------------------
# Actual vs Predicted (TEST set)
# ---------------------------
plt.figure()
plt.scatter(y_test, y_test_pred, alpha=0.5)
plt.plot([y_test.min(), y_test.max()],
         [y_test.min(), y_test.max()],
         color="red", linestyle="--")
plt.xlabel("Actual Profit")
plt.ylabel("Predicted Profit")
plt.title("Actual vs Predicted (Test Set)")
plt.savefig("data/results/actual_vs_predicted.png")
plt.close()

# ---------------------------
# Feature importance (tree models)
# ---------------------------
if hasattr(model, "feature_importances_"):
    importance_df = pd.DataFrame({
        "feature": feature_names,
        "importance": model.feature_importances_
    }).sort_values(by="importance", ascending=False)

    importance_df.to_csv("data/results/feature_importance.csv", index=False)

    plt.figure(figsize=(8, 6))
    plt.barh(
        importance_df["feature"][:10],
        importance_df["importance"][:10]
    )
    plt.gca().invert_yaxis()
    plt.title("Top 10 Feature Importances")
    plt.savefig("data/results/feature_importance.png")
    plt.close()

