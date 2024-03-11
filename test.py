import pandas as pd
import glob
import os
from Extract_pdf_function import extract_pdf

directory_path = r"D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\IA\original file"

pdf_files = glob.glob(os.path.join(directory_path, '**/*.pdf'), recursive=True)

all_tables = []

for pdf_file in pdf_files:
    try:
        print(f"Processing {pdf_file}...")
        df0, df1, df2 = extract_pdf(pdf_file)

        # Inspect and reset index if necessary
        if df0.empty or df1.empty or df2.empty:
            print(f"One of the DataFrames for {pdf_file} is empty. Skipping...")
            continue

        # Resetting index to avoid InvalidIndexError
        df0 = df0.reset_index(drop=True)
        df1 = df1.reset_index(drop=True)
        df2 = df2.reset_index(drop=True)

        tables = pd.concat([df0, df1, df2], ignore_index=True)
        all_tables.append(tables)
        print("Extracted successfully")

    except Exception as e:
        print(f"An error occurred while processing {pdf_file}: {e}")

if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_csv(os.path.join(directory_path, 'combined_extracted_tables.csv'), index=False, header=False)
    print("All tables have been concatenated and saved.")
else:
    print("No tables were extracted or all were empty.")
