from typing import List, Any

import pandas as pd
import glob
import os

from pandas import DataFrame

from Extract_pdf_function import extract_pdf
from Clean_PaymentData_Function0312 import clean_payment

directory_path = r"D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\IA\original file"

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
    PaymentData_df = clean_payment(df1,df2, '1111111')

    # Append the tables to the all_tables list
    all_tables.append(PaymentData_df)

# Concatenate all DataFrames in the list into a single DataFrame after the loop
if all_tables:  # Check if all_tables is not empty
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_csv('combined_extracted_tables_payment.csv', index=False, header=False)
    print("All tables have been concatenated and saved to 'combined_extracted_tables_payment.csv'. ")
