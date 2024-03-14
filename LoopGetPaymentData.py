import glob
import os

import pandas as pd

from Clean_PaymentData_Function0312 import clean_payment
from Extract_pdf_function import extract_pdf
from dbutilities.DBConnection import get_database_engine
from dbutilities.dbColumnsType import sql_dtypes_CommissionPayment

directory_path = r"D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\IA original"

# import os

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
    PaymentData_df = clean_payment(df1, df2, '3333333')

    # For SQL Server Authentication
    engine = get_database_engine()
    sql_dtypes = sql_dtypes_CommissionPayment

    # Writing the DataFrame to the SQL Server table
    PaymentData_df.to_sql('CommissionPayment', con=engine, if_exists='append', index=False, dtype=sql_dtypes)
