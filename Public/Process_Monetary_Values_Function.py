# def process_monetary_values(df, columns):
#     for col in columns:
#         # Remove currency symbol, commas, and parentheses for negative values
#         df[col] = df[col].replace({'\$': '', ',': '', '\(': '-', '\)': ''}, regex=True).astype(float)
#     return df

def Preprocess_Monetary_Values(df, columns):
    for col in columns:
        # Replace empty strings with None
        df[col] = df[col].replace('', None)
        # Remove currency symbol, commas, and parentheses for negative values
        df[col] = df[col].replace({'\$': '', ',': '', '\(': '-', '\)': ''}, regex=True)
        # Convert the column to float
        df[col] = df[col].astype(float)
    return df