import pandas as pd 

def get_pandas_null_cols(df):
    if isinstance(df, pd.Series):
        if df.isnull().any():
            return [df.name]
        return []
    return [col for col in df.columns
            if sum(df[col].isnull()) > 0]
