import pandas as pd
import glob
import os
from PDFextract import extract_pdf
from Clean_CommissionInfo_Function import clean_commissioninfo
from dbutilities.Insert_Database_Function import Insert_Database
from dbutilities.dbColumnsType import sql_dtypes_CommissionInfo


directory_path = r"C:\Users\fanzi\Desktop\AI Financial\Python\iA"

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
    tables = df0
    print("Extracted successfully")

    # Set the value for InstitutionName
    institution_name = 'IA'

    # Call the function to get the cleaned DataFrame
    df_commissioninfo = clean_commissioninfo(df0, institution_name)

    print(df_commissioninfo)


    Insert_Database(df_commissioninfo)