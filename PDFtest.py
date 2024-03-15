from PDFextract import extract_pdf
from PDFprint5 import convert_df_to_single_row

file_path1 = r"D:\Python\AIFAccounting\Jun 26 - July 2, 2021.pdf"

# Extract tables using the defined function extract_details
df0, df1, df2 = extract_pdf(file_path1)

table = df0


 #Set the value for InstitutionName
institution_name = 'IA'

# Call the function to get the cleaned DataFrame
cleaned_dataframe,CommissionID, end_date_year, AdvisorName = convert_df_to_single_row(df0, institution_name)
print(CommissionID, end_date_year, AdvisorName)
print(cleaned_dataframe)

# # Export the cleaned data to a new CSV file
# cleaned_file_path = 'cleaned_data3.csv'
# cleaned_dataframe.to_csv(cleaned_file_path, index=False)
#
# print("Cleaned data has been exported to 'cleaned_data3.csv'.")