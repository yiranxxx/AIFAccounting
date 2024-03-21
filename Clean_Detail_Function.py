import pandas as pd
from Public.Process_Monetary_Values_Function import Preprocess_Monetary_Values
# import os
#
# os.chdir(r"D:\AIF Intern\Accounting\test")
#
# file_name = "2.pdf"
#  # Unpack the tuple


def Clean_Detail(df1, df2, CommissionID):

    # find the row index of 'TRANSFER FROM AFFILIATED'
    index2 = df2[df2.iloc[:, 0] == 'TRANSFER FROM AFFILIATED'].index

    # detect if there is "TRANSFER FROM AFFILIATED" row in df2
    if not index2.empty:
        # remove rows after 'TRANSFER FROM AFFILIATED'
        df2 = df2.iloc[:index2[0]].copy()
        num_col = df2.shape[1]
        # remove empty columns
        if num_col == 12:
            df2.drop(df2.columns[6], axis=1, inplace=True)

        # Reset both column and index labels
        df2.reset_index(drop=True, inplace=True)
        df2.columns = range(len(df2.columns))

        # combine df1 and df2 if df1 exists
        if df1 is not None:
            df2.columns = df1.columns
            # combine two dataframes
            combined_df = pd.concat([df1, df2], ignore_index=True)
        else:
            combined_df = df2
    else:
        if df1 is not None:
            # remove rows after 'TRANSFER FROM AFFILIATED'
            index1 = df1[df1.iloc[:, 0] == 'TRANSFER FROM AFFILIATED'].index
            combined_df = df1.iloc[:index1[0]].copy()

    # Detect rows containing "Total" and remove them
    combined_df = combined_df[~combined_df.apply(lambda row: row.astype(str).str.contains('TOTAL').any(), axis=1)]
    # Reset index after removing rows
    combined_df.reset_index(drop=True, inplace=True)
    # Set data types for all columns
    combined_df = combined_df.astype({0: str, 1: str, 2: str, 4: str})  # Assuming column 0 and 2 are string, and column 1 is integer


    # create commission type column
    # Check for single values in each row, and obtain a list of row indices of single-value rows
    type_indices = []
    for index, row in combined_df.iterrows():
        # Check if only one cell in the row is non-null and non-empty
        if sum(row.notnull() & (row.astype(str).str.strip() != "")) == 1:
            type_indices.append(index)
    # print("Rows with single value indices:", type_indices)

    # Initialize the new column
    new_column_values = []

    # Assign values to the new column based on the index list
    for i in range(len(combined_df)):
        if i in type_indices:
            value = combined_df.iloc[i, 0]
        new_column_values.append(value)

    # Add the new column to the DataFrame
    combined_df[11] = new_column_values
    combined_df = combined_df.drop(type_indices, axis=0)
    combined_df.insert(0, None, CommissionID)
    # Assuming combined_df is your existing DataFrame
    columns = ['CommissionID', 'CustomerName', 'ContractNumber', 'CoverageName',
               'TransactionDate', 'TransactionType', 'CompensationBasisAmount',
               'RPLPer', 'SharPer', 'CommPer', 'AmountDue', 'Balance', 'CommissionType']

    # Assign the column names to combined_df
    combined_df.columns = columns
    # Preprocess monetary values
    monetary_columns = ['CompensationBasisAmount', 'AmountDue', 'Balance']
    df_detail = Preprocess_Monetary_Values(combined_df, monetary_columns)
    df_detail.replace({'': None}, inplace=True)
    #df_detail = pd.concat([combined_df])

    return df_detail

# CommissionID = "333"
# from Extract_pdf import extract_pdf
# _, df1, df2 = extract_pdf(file_name)
#
# # test
# df_detail = clean_detail(df1, df2, CommissionID)
# df_detail.to_csv('extract_test.csv', index=False)

# print(combined_df)

# Remove '$' sign from all cells
#combined_df = combined_df.apply(lambda x: x.str.replace('$', '') if x.dtype == 'object' else x)