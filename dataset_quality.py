import pandas as pd

def calculate_dataset_quality(df):

    total_cells = df.shape[0] * df.shape[1]

    missing_values = df.isnull().sum().sum()

    duplicate_rows = df.duplicated().sum()

    # Missing value penalty
    missing_penalty = (missing_values / total_cells) * 100

    # Duplicate penalty
    duplicate_penalty = duplicate_rows * 5

    quality = 100 - missing_penalty - duplicate_penalty

    if quality < 0:
        quality = 0

    return {
        "missing": int(missing_values),
        "duplicates": int(duplicate_rows),
        "quality": round(quality)
    }