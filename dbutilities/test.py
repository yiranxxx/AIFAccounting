from sqlalchemy.types import String, Date, Numeric

# Assuming these modules are available in your Python environment
from Clean_PaymentData_Function0312 import clean_payment
from Extract_pdf_function import extract_pdf
from dbutilities.DBConnection import get_database_engine
from dbutilities.dbColumnsType import sql_dtypes_CommissionPayment

file_path = r"D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\IA original\original file\Apr 2 - Apr 8, 2022.pdf"

# Error handling for PDF extraction
df0, df1, df2 = extract_pdf(file_path)

PaymentData_df = clean_payment(df1, df2, '123233444')

# Preprocess monetary columns to convert them to float


# For SQL Server Authentication
engine = get_database_engine()
sql_dtypes = sql_dtypes_CommissionPayment


# Writing the DataFrame to the SQL Server table
PaymentData_df.to_sql('CommissionPayment', con=engine, if_exists='append', index=False, dtype=sql_dtypes)



