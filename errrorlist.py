import pandas as pd

# Path to the Excel file
file_name = r"D:\AccountingProject\Logfile\Errorlist.xlsx"

# Read the Excel file into a DataFrame
error_df = pd.read_excel(file_name)

# Assuming you want to extract the second column, which is indexed as 1
# If you know the column name, it's better to use it directly, e.g., error_df['ColumnName']
pdf_files = error_df.iloc[:, 1]  # This extracts all rows of the second column

# Print the extracted column values
print(pdf_files)