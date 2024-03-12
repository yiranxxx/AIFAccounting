import camelot
import os
import pdfplumber
import pandas as pd

# directory_path = r"D:\AIF Intern\Accounting\test"
# # Change the working directory to the specified path
# os.chdir(directory_path)

# sdddddddddd
def extract_pdf(file_name):
    df0 = None    # header information
    df1 = None    # for report with multiple pages, commission details from page 3 to the page before last page
    df2 = None    # commission details of last page (if the report only has 3 pages, then it is the information of page 3)
    # extract report header info
    header_coordinates = ['0,610,770,500']
    tables0 = camelot.read_pdf(file_name, flavor='stream', pages="3", table_areas=header_coordinates)
    df0 = tables0[0].df

    # extract commission details
    with pdfplumber.open(file_name) as pdf:
        # Get the number of pages in the PDF
        last_page = len(pdf.pages)
    page_range = '3-' + str(last_page - 1)
    table_coordinates = ['0,450,850,45']
    min_row_num1 = 6  # minimum number of rows for multiple with only one record
    min_row_num2 = 7  # minimum number of rows for single with only one record

    if int(last_page) > 3:

        # extract contents from page 3 to the page before the last page
        tables1 = camelot.read_pdf(file_name, flavor='stream', pages=page_range,
                                   table_areas=table_coordinates, row_tol=10)

        for table in tables1:
            # Check the number of columns in the table
            num_columns = table.shape[1]

            # If the table has 11 columns, move to the next table
            if num_columns == 11:
                continue

            # If the table has 9 columns, add 2 columns after column 6
            elif num_columns == 9:
                # Insert two empty columns after column 6
                table.df.insert(loc=6, column=None, value='')
                table.df.insert(loc=7, column=None, value='')

        # Initialize an empty list to store DataFrames
        dfs = []

        # Iterate over tables and append them to the list
        for table in tables1:
            dfs.append(table.df)

        # Concatenate all DataFrames in the list into a single DataFrame
        df1 = pd.concat(dfs, ignore_index=True)

        # extract contents from the last page
        last_page_test1 = camelot.read_pdf(file_name, flavor='stream', pages=str(last_page),
                                           table_areas=table_coordinates, row_tol=10)
        num_rows1 = last_page_test1[0].df.shape[0]

        if num_rows1 <= min_row_num1:
            tables2 = camelot.read_pdf(file_name, flavor='stream', pages=str(last_page),
                                       table_areas=table_coordinates, column_tol=-30, row_tol=10)
        else:
            tables2 = camelot.read_pdf(file_name, flavor='stream', pages=str(last_page),
                                       table_areas=table_coordinates, row_tol=10)

            # Extract the DataFrame from the Camelot Table
        df2 = tables2[0].df


    else:
        last_page_test2 = camelot.read_pdf(file_name, flavor='stream', pages='3',
                                           table_areas=table_coordinates, row_tol=10)
        num_rows2 = last_page_test2[0].df.shape[0]

        if num_rows2 <= min_row_num2:
            tables2 = camelot.read_pdf(file_name, flavor='stream', pages='3',
                                       table_areas=table_coordinates, column_tol=-30, row_tol=10)
        else:
            tables2 = camelot.read_pdf(file_name, flavor='stream', pages='3',
                                       table_areas=table_coordinates, row_tol=10)
        df2 = tables2[0].df

    return df0, df1, df2


