import camelot
import os
import pdfplumber
import pandas as pd

# directory_path = r"\\192.168.2.8\AIF_Interns\202312\Accounting\ErrorFile"
# # Change the working directory to the specified path
# os.chdir(directory_path)
# file_name = "Aug 21 - Aug 27, 2021.pdf"

def Extract_PDF(file_name):
    df0 = None  # header information
    df1 = None  # for report with multiple pages, details from page 3 to the page before last page
    df2 = None  # details of last page (if the report only has 3 pages, then it is the details of Page 3)
    # extract report header info

    # extract commission details
    with pdfplumber.open(file_name) as pdf:
        # Get the number of pages in the PDF
        last_page = len(pdf.pages)
    page_range = '3-' + str(last_page - 1)
    table_coordinates = ['0,450,850,40']
    min_row_num1 = 6  # minimum number of rows for multiple with only one record
    min_row_num2 = 10  # minimum number of rows for single with only one record

    if int(last_page) > 3:
        header_coordinates = ['0,610,770,500']
        tables0 = camelot.read_pdf(file_name, flavor='stream', pages="3", table_areas=header_coordinates)
        df0 = tables0[0].df

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
            elif num_columns == 10:
                # Insert two empty columns after column 6
                table.df.insert(loc=6, column=None, value='')

        # Initialize an empty list to store DataFrames
        dfs = []
        # Iterate over tables and append them to the list
        for table in tables1:
            dfs.append(table.df.reset_index(drop=True))  # Reset index before appending

        # Concatenate all DataFrames in the list into a single DataFrame
        df1 = pd.concat(dfs, ignore_index=True)

        # extract contents from the last page
        last_page_test1 = camelot.read_pdf(file_name, flavor='stream', pages=str(last_page),
                                           table_areas=table_coordinates, row_tol=10)
        num_rows1 = last_page_test1[0].df.shape[0]

        if num_rows1 <= min_row_num1:
            tables2 = camelot.read_pdf(file_name, flavor='stream', pages=str(last_page),
                                       table_areas=table_coordinates, column_tol=-40, row_tol=10)
        else:
            tables2 = camelot.read_pdf(file_name, flavor='stream', pages=str(last_page),
                                       table_areas=table_coordinates, row_tol=10)

        df2 = tables2[0].df.reset_index(drop=True)  # Reset index for the last page table

    elif int(last_page) == 3:
        header_coordinates = ['0,610,770,500']
        tables0 = camelot.read_pdf(file_name, flavor='stream', pages="3", table_areas=header_coordinates)
        df0 = tables0[0].df

        last_page_test2 = camelot.read_pdf(file_name, flavor='stream', pages='3',
                                           table_areas=table_coordinates, row_tol=10)
        num_rows2 = last_page_test2[0].df.shape[0]

        if num_rows2 <= min_row_num2:
            tables2 = camelot.read_pdf(file_name, flavor='stream', pages='3',
                                       table_areas=table_coordinates, column_tol=-40, row_tol=10)
        else:
            tables2 = camelot.read_pdf(file_name, flavor='stream', pages='3',
                                       table_areas=table_coordinates, row_tol=10)
        df2 = tables2[0].df.reset_index(drop=True)  # Reset index for the last page table
    elif int(last_page) < 3:
        df0 = None
        df1 = None
        df2 = None


    return df0, df1, df2

# test
# _, df1, _ = Extract_PDF(file_name)
# df1.to_csv('test.csv', index=False, header=False)




#  Assuming extract_pdf() function returns df0, df1, and df2
# _, df1, df2 = extract_pdf(file_name)
#
# df2.columns = df1.columns
# # combine two dataframes
# combined_df = pd.concat([df1, df2], ignore_index=True)
#
# # Saving the combined DataFrame to CSV
# combined_df.to_csv('extract_test.csv', index=False, header=False)

'''
        indices = df2[df2.iloc[:, 0] == 'TRANSFER FROM AFFILIATED'].index

    if not indices.empty:
        df2 = df2.iloc[:indices[0]].copy()
        df2.drop(df2.columns[6], axis=1, inplace=True)
        df2.columns = df1.columns

        # combine two dataframes
        combined_df = pd.concat([df1, df2], ignore_index=True)
        combined_df.to_csv('extract_all.csv', index=False, header=False)

else
#df2.to_csv('extract_detail2.csv', index= False, header=False)


# combine two dataframes
combined_df = pd.concat([df1, df2], ignore_index=True)

combined_df.to_csv('extract_all.csv', index=False, header=False)


# Remove the 7th column (index 6) from the DataFrame
#df.drop(df.columns[6], axis=1, inplace=True)

#indices = df[df.iloc[:, 0] == 'TRANSFER FROM AFFILIATED'].index
#print(indices)



#print(tables[1])
# Plot contour
#camelot.plot(tables[0], kind='grid').show()
#columns = [155, 205, 270, 335, 455, 520, 550, 575, 620, 710]
#camelot.plot(tables[0], kind='contour').show()
#tables.export('foo.csv', f='csv')
#tables[0].to_csv('extract_detail.csv')

#camelot.plot(tables[0], kind='contour').show()
'''
