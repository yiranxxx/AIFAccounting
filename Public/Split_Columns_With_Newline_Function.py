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
