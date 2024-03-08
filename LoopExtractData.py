import datetime
import re
import pandas as pd
import glob
import os

from Extract_wholeData_from_pdf import extract_wholetext_from_pdf, extract_wholetables_from_pdf



directory_path = r'\\AIF-NAS01\AIF_Interns\202312\Accounting\Template\IA'

# Change the working directory to the specified path
os.chdir(directory_path)

# Find all PDF files in the directory and its subdirectories
pdf_files = glob.glob('**/*.pdf', recursive=True)


# Initialize an empty list to store DataFrames from all PDFs
all_tables = []
# Loop through each PDF file and extract tables
for pdf_file in pdf_files:
    print(pdf_file)
    # Assume extract_wholetables_from_pdf returns a single DataFrame or a list of DataFrames
    tables = extract_wholetables_from_pdf(pdf_file)
    print("Extracted successfully")

    # Append the tables to the all_tables list
    # If tables is a single DataFrame, use append. If it's a list of DataFrames, use extend.
    if isinstance(tables, pd.DataFrame):  # Check if tables is a single DataFrame
        all_tables.append(tables)
    else:  # If tables is a list of DataFrames
        all_tables.extend(tables)

# Concatenate all DataFrames in the list into a single DataFrame after the loop
if all_tables:  # Check if all_tables is not empty
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_csv('combined_extracted_tables.csv', index=False)
    print("All tables have been concatenated and saved to 'combined_extracted_tables.csv'.")