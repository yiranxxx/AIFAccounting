def Preprocess_Monetary_Values(df, columns):
    for col in columns:
        # Remove currency symbol, commas, and parentheses for negative values
        df[col] = df[col].replace({'\$': '', ',': '', '\(': '-', '\)': ''}, regex=True).astype(float)
    return df