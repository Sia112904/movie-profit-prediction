# src/feature_engineering.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# ️⃣ Load the cleaned dataset
df = pd.read_csv("data/processed/cleaned_movies.csv")

# ️⃣ Select features
# Use 'vote_average' instead of 'rating'
feature_cols = [
    "budget",
    "runtime",
    "release_year",
    "vote_average"
]

# Include all one-hot encoded genre columns
genre_cols = [
    "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
    "Drama", "Family", "Fantasy", "Foreign", "History", "Horror", "Music",
    "Mystery", "Romance", "Science Fiction", "TV Movie", "Thriller", "War", "Western"
]

all_features = feature_cols + genre_cols

X = df[all_features]

#️⃣ Target variable (profit)
y = df["revenue"] - df["budget"]  # simple profit calculation

#️ Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

#  Scale numeric features (budget, runtime, release_year, vote_average)
numeric_features = ["budget", "runtime", "release_year", "vote_average"]
scaler = StandardScaler()
X_train[numeric_features] = scaler.fit_transform(X_train[numeric_features])
X_test[numeric_features] = scaler.transform(X_test[numeric_features])

# Save ML-ready datasets
X_train.to_csv("data/processed/X_train.csv", index=False)
X_test.to_csv("data/processed/X_test.csv", index=False)
y_train.to_csv("data/processed/y_train.csv", index=False)
y_test.to_csv("data/processed/y_test.csv", index=False)

print(" Feature engineering complete. ML-ready datasets saved in data/processed/")

