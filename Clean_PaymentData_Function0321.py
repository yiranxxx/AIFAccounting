import pandas as pd

from Extract_pdf_function import Extract_PDF
from Public.Process_Monetary_Values_Function import process_monetary_values
from dbutilities.Database_Function import Insert_DB

# Define the file path
file_name = r"D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\IA original\Advisor1\iA\Aug 20 - Aug 26, 2022.pdf"

# Unpack the returned tuple into df0, df1, and df2
df0, df1, df2 = Extract_PDF(file_name)


def clean_payment(df1, df2, CommissionID):

    if df1 is None or df1.empty:
        raw_df = df2
    else:
        df2.columns = df1.columns
        # combine two dataframes
        combined_df = pd.concat([df1, df2], ignore_index=True)
        raw_df = pd.concat([df1, df2], ignore_index=True)

    raw_df.to_csv(r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\CombineData.csv', index=False, header=True)

    # Find indices of rows that contain 'TRANSFER FROM AFFILIATED'
    indices_with_payment = raw_df[
        raw_df.apply(lambda row: 'TRANSFER FROM AFFILIATED' in row.astype(str).values, axis=1)
    ].index

    # Determine the last index from the filtered indices, if available
    if len(indices_with_payment) > 0:
        last_transfer_index = indices_with_payment[-1]
        PaymentType = "TRANSFER FROM AFFILIATED"

    # Find indices of rows that contain 'LICENCE CONTROL'
    indices_with_payment = raw_df[
        raw_df.apply(lambda row: 'LICENCE CONTROL' in row.astype(str).values, axis=1)
    ].index

    # Determine the last index from the filtered indices, if available
    if len(indices_with_payment) > 0:
        last_transfer_index = indices_with_payment[-1]
        PaymentType = "LICENCE CONTROL"

    # Subtracting 2 from the actual last index of the raw DataFrame
    last_row_index = raw_df.index[-1] - 2
    sliced_df = raw_df.iloc[last_transfer_index + 1:last_row_index + 1]
    sliced_df.to_csv(r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\CombineData2.csv', index=False, header=True)

    # Retrieve the last row of the DataFrame
    last_row = raw_df.iloc[-1]

    # Find the last non-null and non-empty value in the last row
    CurrentBalance = next((value for value in last_row[::-1] if pd.notnull(value) and value != ''), None)

    print(CurrentBalance)
    sliced_df.to_csv(r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\CombineData3.csv', index=False, header=True)

    # Transformations and creating a new DataFrame in the same step
    cleaned_df = pd.DataFrame({
        'CommissionID': CommissionID,
        'PaymentType': PaymentType,
        'CompanyCode': sliced_df[0].str.extract(r'\((.*?)\)')[0],  # Extracting value inside parentheses
        'PayToName': sliced_df[0].str.split(r'\)').str[1],  # Extracting value after the closing parenthesis
        'TransactionDate': sliced_df[1],  # Taking the value as is
        'TransactionType': sliced_df[2],  # Taking the value as is
        'CommPer': sliced_df.iloc[:, -3],  # Getting the third column from the end
        'AmountDue': sliced_df.iloc[:, -2],  # Getting the second column from the end
        'Balance': sliced_df.iloc[:, -1],  # Getting the last column
        'CurrentBalance': CurrentBalance,
    })
    cleaned_df.to_csv(r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\CombineData5.csv', index=False, header=True)
    # Preprocess monetary values
    monetary_columns = ['AmountDue', 'Balance', 'CurrentBalance']
    df = process_monetary_values(cleaned_df, monetary_columns)

    # Data type conversions
    df['CommissionID'] = df['CommissionID'].astype(str)
    df['PaymentType'] = df['PaymentType'].astype(str)
    df['CompanyCode'] = df['CompanyCode'].astype(str)
    df['PayToName'] = df['PayToName'].astype(str)
    df['TransactionType'] = df['TransactionType'].astype(str)
    df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
    df['CommPer'] = df['CommPer'].astype(float)

    # Displaying the new DataFrame
    df_payment = df
    print(df_payment)

    df_payment.to_csv(r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\CombineData4.csv', index=False, header=True)
    return df_payment


CommissionID = "111111"
PaymentData_df = clean_payment(df1, df2, CommissionID)
Insert_DB(PaymentData_df)
