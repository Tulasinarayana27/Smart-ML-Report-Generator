import pandas as pd
from sklearn.preprocessing import LabelEncoder


def preprocess_dataset(df):

    # Remove duplicates
    df = df.drop_duplicates()

    # Fill missing values
    for column in df.columns:

        if pd.api.types.is_numeric_dtype(df[column]):
            df[column] = df[column].fillna(df[column].mean())

        else:
            df[column] = df[column].fillna(df[column].mode()[0])

    # Encode categorical columns
    encoder = LabelEncoder()

    for column in df.columns:

        if df[column].dtype == "object":
            df[column] = encoder.fit_transform(df[column].astype(str))

    return df