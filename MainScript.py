from PDFextract import extract_pdf
from Clean_CommissionInfo_Function import clean_commissioninfo
from dbutilities.Insert_Database_Function import Insert_Database
from dbutilities.dbColumnsType import sql_dtypes_CommissionInfo

file_path1 = r"D:\Python\AIFAccounting\Jun 26 - July 2, 2021.pdf"

# Extract tables using the defined function extract_details
df0, df1, df2 = extract_pdf(file_path1)

table = df0

# Set the value for InstitutionName
institution_name = 'IA'

# Call the function to get the cleaned DataFrame
df_commissioninfo = clean_commissioninfo(df0, institution_name)

print(df_commissioninfo)
table.to_csv('test2.csv', index=False)

Insert_Database(df_commissioninfo)
