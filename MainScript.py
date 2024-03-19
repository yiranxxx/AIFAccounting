# from PDFextract import extract_pdf
# from Clean_CommissionInfo_Function import clean_commissioninfo
# from dbutilities.Insert_Database_Function import Insert_Database
# from Data_Insertion_Check import Insert_Database
# from dbutilities.dbColumnsType import sql_dtypes_CommissionInfo


from PDFextract import extract_pdf
from Clean_CommissionInfo_Function import clean_commissioninfo
from dbutilities.Insert_Database_Function import Insert_Database
from dbutilities.dbColumnsType import sql_dtypes_CommissionInfo
from sqlalchemy import create_engine, MetaData, Table, select

# Database connection information
server = '192.168.2.86'
port = '1433'
database = 'AIF_Test'
user = 'AccountingTest'
password = '1234qwer'

# Create database URI
db_uri = f'mssql+pymssql://{user}:{password}@{server}:{port}/{database}'

# Create SQLAlchemy engine
engine = create_engine(db_uri)

# Function to get existing Commission IDs from the database
def get_existing_commission_ids(engine):
    with engine.connect() as conn:
        metadata = MetaData()
        # Reflect CommissionInfo table from the database
        commission_info_table = Table('CommissionInfo', metadata, autoload_with=engine)
        # Create a select statement to fetch existing commission IDs
        select_statement = select([commission_info_table.columns.CommissionID])
        existing_commission_ids = conn.execute(select_statement).fetchall()
        return {row[0] for row in existing_commission_ids}

file_path1 = r"D:\Python\AIFAccounting\Jun 26 - July 2, 2021.pdf"

# Extract tables using the defined function extract_details
df0, df1, df2 = extract_pdf(file_path1)

table = df0

# Set the value for InstitutionName
institution_name = 'IA'

# Call the function to get the cleaned DataFrame
df_commissioninfo = clean_commissioninfo(df0, institution_name)

print(df_commissioninfo)

# Get existing commission IDs from the database
existing_commission_ids = get_existing_commission_ids(engine)

# Filter out rows with existing commission IDs from the DataFrame
df_to_insert = df_commissioninfo[~df_commissioninfo['CommissionID'].isin(existing_commission_ids)]

# Insert only the filtered DataFrame
Insert_Database(df_to_insert)


# from PDFextract import extract_pdf
# from Clean_CommissionInfo_Function import clean_commissioninfo
# from dbutilities.Insert_Database_Function import Insert_Database
# from dbutilities.dbColumnsType import sql_dtypes_CommissionInfo
# from sqlalchemy import create_engine, MetaData, Table, select
#
# # Database connection information
# server = '192.168.2.86'
# port = '1433'
# database = 'AIF_Test'
# user = 'AccountingTest'
# password = '1234qwer'
#
# # Create database URI
# db_uri = f'mssql+pymssql://{user}:{password}@{server}:{port}/{database}'
#
# # Create SQLAlchemy engine
# engine = create_engine(db_uri)
#
# # Function to get existing Commission IDs from the database
# def get_existing_commission_ids(engine):
#     with engine.connect() as conn:
#         metadata = MetaData()
#         # Reflect CommissionInfo table from the database
#         commission_info_table = Table('CommissionInfo', metadata, autoload_with=engine)
#         # Execute a select query to fetch existing commission IDs
#         select_statement = select([commission_info_table.c.CommissionID])
#         existing_commission_ids = conn.execute(select_statement).fetchall()
#         return [row[0] for row in existing_commission_ids]
#
# file_path1 = r"D:\Python\AIFAccounting\Jun 26 - July 2, 2021.pdf"
#
# # Extract tables using the defined function extract_details
# df0, df1, df2 = extract_pdf(file_path1)
#
# table = df0
#
# # Set the value for InstitutionName
# institution_name = 'IA'
#
# # Call the function to get the cleaned DataFrame
# df_commissioninfo = clean_commissioninfo(df0, institution_name)
#
# print(df_commissioninfo)
#
# # Get existing commission IDs from the database
# existing_commission_ids = get_existing_commission_ids(engine)
#
# # Filter out rows with existing commission IDs from the DataFrame
# df_to_insert = df_commissioninfo[~df_commissioninfo['CommissionID'].isin(existing_commission_ids)]
#
# # Insert only the filtered DataFrame
# Insert_Database(df_to_insert)
#



# file_path1 = r"D:\Python\AIFAccounting\Jun 26 - July 2, 2021.pdf"
#
# # Extract tables using the defined function extract_details
# df0, df1, df2 = extract_pdf(file_path1)
#
# table = df0
#
# # Set the value for InstitutionName
# institution_name = 'IA'
#
# # Call the function to get the cleaned DataFrame
# df_commissioninfo = clean_commissioninfo(df0, institution_name)
#
# print(df_commissioninfo)
# # table.to_csv('test2.csv', index=False)
#
# Insert_Database(df_commissioninfo)
