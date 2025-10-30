import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler, LabelEncoder


def handle_missing_values(df: pd.DataFrame):
    for col in df.columns:
        if df[col].dtype in ['int64', 'float64']:
            df[col].fillna(df[col].mean(), inplace=True)
        else:
            df[col].fillna(df[col].mode()[0], inplace=True)
    return df


def encode_categorical(df: pd.DataFrame):
    label_encoder = LabelEncoder()
    cat_cols = df.select_dtypes(include=['object']).columns
    
    for col in cat_cols:
        df[col] = label_encoder.fit_transform(df[col].astype(str))
    
    return df

def remove_outliers(df: pd.DataFrame):
    numeric_cols = df.select_dtypes(include=['number']).columns
    
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        df = df[(df[col] >= Q1 - 1.5 * IQR) & (df[col] <= Q3 + 1.5 * IQR)]
    
    return df

def normalize_columns(df: pd.DataFrame, columns: list):
    scaler = MinMaxScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df


def standardize_columns(df: pd.DataFrame, columns: list):
    scaler = StandardScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df


def full_preprocess_pipeline(df: pd.DataFrame):
    df = handle_missing_values(df)
    df = encode_categorical(df)
    df = remove_outliers(df)
    return df
