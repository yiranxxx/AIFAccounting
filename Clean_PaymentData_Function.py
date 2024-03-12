from Extract_pdf_function import extract_pdf
import pandas as pd

# # Define the file path
# file_name = r"D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\IA\original file\Feb 5 - Feb 11, 2022.pdf"
#
# # Unpack the returned tuple into df0, df1, and df2
# df0, df1, df2 = extract_pdf(file_name)
# raw_df = df2

##seegesrgsehgsrghsw


def clean_PaymentData(raw_df):
    # Find rows that contain 'TRANSFER FROM AFFILIATED'
    row_indices = raw_df[raw_df.apply(lambda row: 'TRANSFER FROM AFFILIATED' in row.astype(str).values, axis=1)].index
    if len(row_indices) > 0:
        number = row_indices[0]
        next_row = raw_df.iloc[number + 1]
        CompanyCode = next_row[0][next_row[0].find('(') + 1:next_row[0].find(')')]
        PayToName = next_row[0][next_row[0].find(')') + 1:].strip()

        # Extracting the first non-null values after PayToName for the details
        details = [value for value in next_row[1:] if pd.notnull(value) and value != '']
        TransactionDate, TransactionType, CommPer, AmountDue, Balance = details[:5]

        # Getting the CurrentBalance from the last non-null and non-empty cell in the row below the identified row
        balance_row = raw_df.iloc[number + 2]
        CurrentBalance = next((value for value in reversed(balance_row) if pd.notnull(value) and value != ''), None)

        print("Extract")

        # Create a DataFrame with the extracted data
        df = pd.DataFrame(
            [[CompanyCode, PayToName, TransactionDate, TransactionType, CommPer, AmountDue, Balance, CurrentBalance]],
            columns=['CompanyCode', 'PayToName', 'TransactionDate', 'TransactionType', 'CommPer', 'AmountDue',
                     'Balance', 'CurrentBalance'])
        return df
    else:
        number = -1
        next_row = raw_df.iloc[number + 1]
        CompanyCode = next_row[0][next_row[0].find('(') + 1:next_row[0].find(')')]
        PayToName = next_row[0][next_row[0].find(')') + 1:].strip()

        # Extracting the first non-null values after PayToName for the details
        details = [value for value in next_row[1:] if pd.notnull(value) and value != '']
        TransactionDate, TransactionType, CommPer, AmountDue, Balance = details[:5]

        # Getting the CurrentBalance from the last non-null and non-empty cell in the row below the identified row
        balance_row = raw_df.iloc[number + 2]
        CurrentBalance = next((value for value in reversed(balance_row) if pd.notnull(value) and value != ''), None)

        print("Extract")

        # Create a DataFrame with the extracted data
        df = pd.DataFrame(
            [[CompanyCode, PayToName, TransactionDate, TransactionType, CommPer, AmountDue, Balance, CurrentBalance]],
            columns=['CompanyCode', 'PayToName', 'TransactionDate', 'TransactionType', 'CommPer', 'AmountDue',
                     'Balance', 'CurrentBalance'])
        return df


# PaymentData_df = clean_PaymentData(raw_df)
#
# print(PaymentData_df)
#
# # Write the DataFrame to a CSV file
# PaymentData_df.to_csv(r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\PaymentData.csv', index=False, header=True)
# print("Payment data has been saved to 'PaymentData.csv'.")
