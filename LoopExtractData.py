
import pandas as pd
import glob
import os

from Extract_pdf_function import extract_pdf

directory_path = r"\\AIF-NAS01\AIF_Interns\202312\Accounting\Template\IA\original file"

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
    tables = df1
    print("Extracted successfully")

    # Append the tables to the all_tables list
    all_tables.append(tables)
    print("appending successfully")
# Concatenate all DataFrames in the list into a single DataFrame after the loop
if all_tables:  # Check if all_tables is not empty
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_csv('combined_extracted_tables_df1.csv', index=False, header=False)
    print("All tables have been concatenated and saved to 'combined_extracted_tables.csv'.")
