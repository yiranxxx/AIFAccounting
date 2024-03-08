import pdfplumber
import camelot
import os
import pandas as pd

# pdf_path = r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\Jun 26 - July 2, 2021 - Mock.pdf'


def extract_wholetext_from_pdf(pdf_path):
    text: str = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Adjusting x_tolerance for better handling of spaces
            text += page.extract_text(x_tolerance=1) + '\n'  # Adding a newline character for separation between pages
    return text


# content = extract_wholetext_from_pdf(pdf_path)
# print(content)


# Change the working directory to the project folder
# os.chdir(r'\\AIF-NAS01\AIF_Interns\202312\Accounting\Template\IA')
# pdffile = 'Dec 3 - Dec 9, 2022.pdf'


def extract_wholetables_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        last_page = len(pdf.pages)  # Get the number of pages in the PDF

    dfs = []  # Initialize an empty list to store DataFrames
    table_coordinates = ['0,450,850,45']  # Specify table areas

    if last_page > 3:
        page_range = '3-' + str(last_page - 1)

        # Extract contents from page 3 to the page before the last page
        tables1 = camelot.read_pdf(file, flavor='stream', pages=page_range, table_areas=table_coordinates, row_tol=10)

        for table in tables1:
            dfs.append(table.df)

        # Extract contents from the last page with different column_tol
        tables2 = camelot.read_pdf(file, flavor='stream', pages=str(last_page), table_areas=table_coordinates, row_tol=10)

        for table in tables2:
            dfs.append(table.df)

    else:
        # Extract contents from the last page if total pages are less than or equal to 4
        tables = camelot.read_pdf(file, flavor='stream', pages=str(last_page) , table_areas=table_coordinates,  row_tol=10)

        for table in tables:
            dfs.append(table.df)

    combined_df = pd.concat(dfs, ignore_index=True)
    return combined_df



    # # Read PDF using camelot with the 'stream' flavor for all pages
    # tables = camelot.read_pdf(file, flavor='stream', pages="3-end")
    #
    # # Create an empty list to store DataFrames
    # dfs = []
    #
    # # Iterate over each extracted table
    # for table in tables:
    #     # Append the DataFrame representation of each table to the list
    #     dfs.append(table.df)
    #
    # # Concatenate all DataFrames in the list into a single DataFrame
    # combined_df = pd.concat(dfs, ignore_index=True)
    # return combined_df

# Save the combined DataFrame to a CSV file
# combineddata = extract_wholetables_from_pdf (pdffile)
#
#
# combineddata .to_csv('combined_extracted_tables.csv', index=False)
#
# print("All tables have been concatenated and saved to 'combined_extracted_tables.csv'.")