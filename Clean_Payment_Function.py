import numpy as np
import pandas as pd
import warnings

from Public.Process_Monetary_Values_Function import Preprocess_Monetary_Values


def Clean_Payment(df1, df2, CommissionID):

    if df1 is None or df1.empty:
        raw_df = df2
    else:
        df1.to_csv(r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\RawData_Df1.csv', index=False, header=True)
        df2.to_csv(r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\RawData_Df2.csv', index=False, header=True)

        if df1.shape[1] == df2.shape[1]:
            df2.columns = df1.columns
        elif df1.shape[1] > df2.shape[1]:
            # Calculate the number of additional columns needed
            additional_columns_needed = df1.shape[1] - df2.shape[1]

            # Generate new column names
            new_column_names = [str(df2.shape[1] + i) for i in range(additional_columns_needed)]

            # Create a DataFrame with the additional columns, filled with NaN
            new_columns_df = pd.DataFrame(columns=new_column_names, index=df2.index).fillna(pd.NA)

            # Concatenate the new columns to df2
            df2 = pd.concat([df2, new_columns_df], axis=1)

            # Update column names to ensure consistency after the extension
            df2.columns = [str(i) for i in range(df1.shape[1])]
            df1.columns = [str(i) for i in range(df1.shape[1])]
        elif df1.shape[1] < df2.shape[1]:
            # Calculate the number of additional columns needed
            additional_columns_needed = df2.shape[1] - df1.shape[1]

            # Generate new column names
            new_column_names = [str(df2.shape[1] + i) for i in range(additional_columns_needed)]

            # Create a DataFrame with the additional columns, filled with NaN
            new_columns_df = pd.DataFrame(columns=new_column_names, index=df1.index).fillna(pd.NA)

            # Concatenate the new columns to df2
            df1 = pd.concat([df1, new_columns_df], axis=1)

            # Update column names to ensure consistency after the extension
            df2.columns = [str(i) for i in range(df1.shape[1])]
            df1.columns = [str(i) for i in range(df1.shape[1])]

        df1.to_csv(r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\RawData_Df1_2.csv', index=False, header=True)
        df2.to_csv(r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\RawData_Df2_2.csv', index=False, header=True)
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
    sliced_df = raw_df.iloc[last_transfer_index + 1:last_row_index + 1].copy()
    sliced_df.to_csv(r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\CombineData_paymentdetail.csv', index=True, header=True)

    # Retrieve the last row of the DataFrame
    last_row = raw_df.iloc[-1]

    # Find the last non-null and non-empty value in the last row
    CurrentBalance = next((value for value in last_row[::-1] if pd.notnull(value) and value != ''), None)

    print(CurrentBalance)

    # Replace empty strings with NaN first
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)
        # Your replace operation here
        sliced_df.replace('', np.nan, inplace=True)

    # Then apply dropna to delete columns where all values are NaN
    deleted_null_df = sliced_df.dropna(axis=1, how='all')

    deleted_null_df = Split_Columns_With_Newline(deleted_null_df)


    # Verifying that columns are properly renamed from '0' to 'n-1'
    new_column_names = [str(i) for i in range(deleted_null_df.shape[1])]
    deleted_null_df.columns = new_column_names

    # Creating cleaned_df with try-except to catch KeyError
    try:
        cleaned_df = pd.DataFrame({
            'CommissionID': CommissionID,
            'PaymentType': PaymentType,
            'CompanyCode': deleted_null_df['0'].str.extract(r'\((.*?)\)')[0],  # Extracting value inside parentheses
            'PayToName': deleted_null_df['0'].str.split(r'\)').str[1],  # Extracting value after the closing parenthesis
            'TransactionDate': deleted_null_df['1'],  # Taking the value as is
            'TransactionType': deleted_null_df['2'],  # Taking the value as is
            'CommPer': deleted_null_df.iloc[:, -3],  # Getting the third column from the end
            'AmountDue': deleted_null_df.iloc[:, -2],  # Getting the second column from the end
            'Balance': deleted_null_df.iloc[:, -1],  # Getting the last column
            'CurrentBalance': CurrentBalance,
        })
    except KeyError as e:
        print(f"Column not found in DataFrame: {e}")

    cleaned_df.to_csv(r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\Cleaneddata.csv', index=True, header=True)
    # Preprocess monetary values
    monetary_columns = ['AmountDue', 'Balance', 'CurrentBalance']
    df = Preprocess_Monetary_Values(cleaned_df, monetary_columns)
    df['CommPer'] = df['CommPer'].astype(float)

    # Displaying the new DataFrame
    df_payment = df
    print(df_payment)
    return df_payment


def Split_Columns_With_Newline(dataframe):
    """
    Splits any columns in the dataframe that contain '\n' and drops the original columns.

    Args:
    dataframe (pd.DataFrame): The DataFrame to operate on.

    Returns:
    pd.DataFrame: The DataFrame with the appropriate columns split.
    """
    # Create a copy of the dataframe to avoid changing the original while iterating
    df = dataframe.copy()

    # Iterate over each column and check for '\n'
    for column in df.columns:
        if df[column].dtype == object and df[column].str.contains('\n', na=False).any():
            # Split the column by '\n'
            split_columns = df[column].str.split('\n', expand=True)

            # Define new column names
            new_column_1 = f"{column}_part1"
            new_column_2 = f"{column}_part2"

            # Insert the split columns into the DataFrame
            column_index = df.columns.get_loc(column)
            df.insert(loc=column_index, column=new_column_1, value=split_columns[0])
            df.insert(loc=column_index + 1, column=new_column_2, value=split_columns[1])

            # Drop the original column
            df.drop(columns=[column], inplace=True)

    return df
