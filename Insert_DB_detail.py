import glob
import os

import pandas as pd

from Clean_Detail import clean_detail
from Extract_pdf import extract_pdf
from DBConnection import get_database_engine
from DBColumnsType import sql_dtypes_CommissionDetail

directory_path = r"D:\AIF Intern\Accounting\test"

# Change the working directory to the specified path
os.chdir(directory_path)

# Find all PDF files in the directory and its subdirectories
pdf_files = glob.glob('**/*.pdf', recursive=True)

# Initialize an empty list to store DataFrames from all PDFs
all_tables = []

# Loop through each PDF file and extract tables
for pdf_file in pdf_files:
    print(pdf_file)
    # Get the full file path
    file_path = os.path.join(directory_path, pdf_file)
    # Extract tables using the defined function extract_details
    df0, df1, df2 = extract_pdf(file_path)
    df_detail = clean_detail(df1, df2, '3333333')

    # For SQL Server Authentication
    engine = get_database_engine()
    sql_dtypes = sql_dtypes_CommissionDetail

    # Writing the DataFrame to the SQL Server table
    df_detail.to_sql('CommissionDetail', con=engine, if_exists='append', index=False, dtype=sql_dtypes)