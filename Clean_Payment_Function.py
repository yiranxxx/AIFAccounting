import pandas as pd
import warnings
import numpy as np

from Public.Process_Monetary_Values_Function import Preprocess_Monetary_Values


def Clean_Payment(DF1, DF2, CommissionID):

    df1 = DF1.copy() if DF1 is not None else None
    df2 = DF2.copy()

    if df1 is None or df1.empty:
        raw_df = df2
    else:
        # df1.to_csv(r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\RawData_Df1.csv', index=False, header=True)
        # df2.to_csv(r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\RawData_Df2.csv', index=False, header=True)

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

        # df1.to_csv(r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\RawData_Df1_2.csv', index=False, header=True)
        # df2.to_csv(r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\RawData_Df2_2.csv', index=False, header=True)
        raw_df = pd.concat([df1, df2], ignore_index=True)
    # raw_df.to_csv(r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\CombineData.csv', index=False, header=True)

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
    # sliced_df.to_csv(r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\CombineData_paymentdetail.csv', index=True, header=True)

    # Retrieve the last row of the DataFrame
    last_row = raw_df.iloc[-1]

    # Find the last non-null and non-empty value in the last row
    CurrentBalance = next((value for value in last_row[::-1] if pd.notnull(value) and value != ''), None)

    # print(CurrentBalance)

    # Replace empty strings with NaN first
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)
        # Your replace operation here
        sliced_df.replace('', np.nan, inplace=True)

    # delete columns where all values are NaN

    deleted_null_df =Delete_Null_And_Left_Shift(sliced_df)
    deleted_null_df = Split_Columns_With_Newline(deleted_null_df)
    # print(deleted_null_df)

    # deleted_null_df.to_csv(r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\CombineData_deleted_null_df.csv', index=True,
    #                  header=True)

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
            'CommPer': deleted_null_df['3'],  # Getting the third column from the end
            'AmountDue': deleted_null_df['4'],  # Getting the second column from the end
            'Balance': deleted_null_df['5'],  # Getting the last column
            'CurrentBalance': CurrentBalance,
        })
    except KeyError as e:
        print(f"Column not found in DataFrame: {e}")

    # cleaned_df.to_csv(r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\Cleaneddata.csv', index=True, header=True)
    # Preprocess monetary values
    monetary_columns = ['AmountDue', 'Balance', 'CurrentBalance']
    df = Preprocess_Monetary_Values(cleaned_df, monetary_columns)
    df['CommPer'] = df['CommPer'].astype(float)

    # Displaying the new DataFrame
    df_payment = df
    # print(df_payment)
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


def Delete_Null_And_Left_Shift(df):
    """
    Shifts non-null values in each row of the DataFrame to the left and fills the remaining positions with NaNs.

    This function is useful for data cleaning and preparation, ensuring that non-null values are aligned to the
    left side of each row, which can be important for subsequent data analysis or processing steps.

    Parameters:
    - df (pd.DataFrame): The input DataFrame to be processed.

    Returns:
    - pd.DataFrame: A new DataFrame with non-null values shifted to the left and NaNs filling the trailing positions.
    """

    # Initialize an empty list to store the processed rows
    new_rows = []

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Filter out null values and collect non-null values
        non_null_values = row.dropna().tolist()

        # Calculate the number of nulls to add to maintain the original row length
        num_nulls = len(row) - len(non_null_values)

        # Create a new row with non-null values followed by nulls
        new_row = non_null_values + [np.nan] * num_nulls

        # Append the new row to the list of processed rows
        new_rows.append(new_row)

    # Create a new DataFrame from the processed rows, preserving the original index and columns
    cleaned_df = pd.DataFrame(new_rows, index=df.index, columns=df.columns)

    return cleaned_df


