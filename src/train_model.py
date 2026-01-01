from data_loader import load_movies
from preprocess import clean_movies
from features import build_features

def main():
    df = load_movies("data/processed/movies.csv")
    df = clean_movies(df)
    X = build_features(df)
    print("Pipeline ran successfully:", X.shape)

if __name__ == "__main__":
    main()

