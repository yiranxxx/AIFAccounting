def Preprocess_Monetary_Values(df, columns):
    for col in columns:
        # Check if the column is not empty and has non-null values before applying operations
        if not df[col].empty and df[col].notnull().any():
            # Replace empty strings with None
            df[col] = df[col].replace('', None)
            # Remove currency symbol, commas, and parentheses for negative values
            df[col] = df[col].replace({'\$': '', ',': '', '\(': '-', '\)': ''}, regex=True)
            # Convert the column to float
            df[col] = df[col].astype(float)
    return df