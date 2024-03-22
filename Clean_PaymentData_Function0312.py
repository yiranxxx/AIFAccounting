
import pandas as pd
from Public.Process_Monetary_Values_Function import process_monetary_values


# Define the file path
file_name = r"D:\AIF Intern\Accounting\Commission\OriginalFile\Advisor1\iA\2022\Aug 27 - Sep 2, 2022(only).pdf"

# Unpack the returned tuple into df0, df1, and df2
df0, df1, df2 = extract_pdf(file_name)


def clean_payment(df1, df2, CommissionID):
    # Rename the column name for concat
    new_column_names11 = [f'{i}' for i in range(11)]
    new_column_names12 = [f'{i}' for i in range(12)]
    new_column_names7 = [f'{i}' for i in range(7)]
    new_column_names10 = [f'{i}' for i in range(10)]

    num_columns2 = df2.shape[1]

    if num_columns2 == 11:
        df2.columns = new_column_names11
    if num_columns2 == 12:
        df2.columns = new_column_names12
    if num_columns2 == 7:
        df2.columns = new_column_names7

    if df1 is None or df1.empty:
        raw_df = df2
    else:
        num_columns1 = df1.shape[1]
        if num_columns1 == 11:
            df1.columns = new_column_names11
        if num_columns1 == 12:
            df1.columns = new_column_names12
        if num_columns1 == 10:
            df1.columns = new_column_names10
        raw_df = pd.concat([df1, df2], ignore_index=True)

    # Find all row indices that contain 'TRANSFER FROM AFFILIATED'
    row_indices = raw_df[raw_df.apply(lambda row: 'TRANSFER FROM AFFILIATED' in row.astype(str).values, axis=1)].index

    if len(row_indices) > 0:
        last_row_index = row_indices[-1]
        next_row = raw_df.iloc[last_row_index + 1]

        CompanyCode = next_row.iloc[0][next_row.iloc[0].find('(') + 1:next_row.iloc[0].find(')')]
        PayToName = next_row.iloc[0][next_row.iloc[0].find(')') + 1:].strip()

        # Extracting the first non-null values after PayToName for the details
        details = [value for value in next_row.iloc[1:] if pd.notnull(value) and value != '']
        TransactionDate, TransactionType, CommPer, AmountDue, Balance = details[:5]

        # Getting the CurrentBalance from the last non-null and non-empty cell in the row below the identified row
        balance_row = raw_df.iloc[last_row_index + 3]
        CurrentBalance = next((balance_row.iloc[i] for i in range(len(balance_row) - 1, -1, -1) if
                               pd.notnull(balance_row.iloc[i]) and balance_row.iloc[i] != ''), None)

        print("Extract")

        # Create a DataFrame with the extracted data
        df = pd.DataFrame(
            [[CommissionID, CompanyCode, PayToName, TransactionDate, TransactionType, CommPer, AmountDue, Balance,
              CurrentBalance]],
            columns=['CommissionID', 'CompanyCode', 'PayToName', 'TransactionDate', 'TransactionType', 'CommPer',
                     'AmountDue',
                     'Balance', 'CurrentBalance'])

        # Preprocess monetary values
        monetary_columns = ['AmountDue', 'Balance', 'CurrentBalance']
        df = process_monetary_values(df, monetary_columns)

        # Data type conversions
        df['CommissionID'] = df['CommissionID'].astype(str)
        df['CompanyCode'] = df['CompanyCode'].astype(str)
        df['PayToName'] = df['PayToName'].astype(str)
        df['TransactionType'] = df['TransactionType'].astype(str)
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
        df['CommPer'] = df['CommPer'].astype(float)


        return df
    else:
        df = pd.DataFrame(
            columns=['CommissionID', 'CompanyCode', 'PayToName', 'TransactionDate', 'TransactionType', 'CommPer',
                     'AmountDue',
                     'Balance', 'CurrentBalance'])



table1 = df1
table2 = df2
table1.to_csv(r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\IA\Table1.csv', index=False,header=True)
table2.to_csv(r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\IA\Table2.csv', index=False,header=True)
raw_df = pd.concat([df1, df2], ignore_index=True)
raw_df.to_csv(r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\IA\CombineData.csv', index=False,header=True)


PaymentData_df = clean_payment(df1, df2)
print(PaymentData_df)
# Write the DataFrame to a CSV file
PaymentData_df.to_csv(r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\IA\PaymentData.csv', index=False,
                      header=True)
print("Payment data has been saved to 'PaymentData.csv'.")
