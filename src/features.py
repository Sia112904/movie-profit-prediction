def build_features(df):
    X = df.select_dtypes(include="number")
    return X

