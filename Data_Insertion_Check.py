from sqlalchemy import create_engine, Table, MetaData, select
from sqlalchemy.exc import IntegrityError
from dbutilities.DBConnection import get_database_engine, connect_db
from dbutilities.dbColumnsType import sql_dtypes_CommissionPayment, sql_dtypes_CommissionInfo

def check_commission_id_exists(db_connection, commission_id):
    cursor = db_connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM CommissionInfo WHERE CommissionID = ?', (commission_id,))
    count = cursor.fetchone()[0]
    return count > 0

db_connection = connect_db()
commission_id_to_check = 'IA_2021-07-02_290327(000)'
exists = check_commission_id_exists(db_connection, commission_id_to_check)
print(exists)

def Insert_Database(df_commissioninfo):
    # Get the database engine
    engine = get_database_engine()

    # Get existing CommissionIDs from the database
    existing_commission_ids = get_existing_commission_ids(engine)

    # Filter out rows with existing CommissionIDs
    df_to_insert = df_commissioninfo[~df_commissioninfo['CommissionID'].isin(existing_commission_ids)]

    if df_to_insert.empty:
        print("All CommissionIDs already exist in the database. No new records inserted.")
        return

    # Insert only the rows with unique CommissionIDs
    df_to_insert.to_sql('CommissionInfo', con=engine, if_exists='append', index=False,
                        dtype=sql_dtypes_CommissionInfo)
    print(f"Inserted {len(df_to_insert)} new records into the CommissionInfo table.")

engine = get_database_engine()
existing_commission_ids= get_existing_commission_ids(engine)
print(existing_commission_ids)

# def Insert_Database(df_CommissionInfo):
#     # Writing the DataFrame to the SQL Server table
#     engine = get_database_engine()
#
#     try:
#         # Establishing a connection
#         conn = engine.connect()
#
#         # Reflecting the existing CommissionInfo table
#         metadata = MetaData()
#         table = Table('CommissionInfo', metadata, autoload_with=engine)
#
#         # Constructing a valid select statement
#         select_statement = select([table.c.CommissionID])
#
#         # Fetching existing CommissionIDs from the database
#         existing_commission_ids = conn.execute(select_statement).fetchall()
#         existing_commission_ids = [row[0] for row in existing_commission_ids]
#
#         # Filter out rows with existing CommissionIDs
#         df_to_insert = df_CommissionInfo[~df_CommissionInfo['CommissionID'].isin(existing_commission_ids)]
#
#         if df_to_insert.empty:
#             print("All CommissionIDs already exist in the database. No new records inserted.")
#             return
#
#         # Insert only the rows with unique CommissionIDs
#         df_to_insert.to_sql('CommissionInfo', con=engine, if_exists='append', index=False,
#                             dtype=sql_dtypes_CommissionInfo)
#         print(f"Inserted {len(df_to_insert)} new records into the CommissionInfo table.")
#
#     finally:
#         # Closing the connection
#         conn.close()
#
#


# def Insert_Database(df_CommissionInfo):
#     # Writing the DataFrame to the SQL Server table
#     engine = get_database_engine()
#
#     try:
#         # Establishing a connection
#         conn = engine.connect()
#
#         # Fetching existing CommissionIDs from the database
#         existing_commission_ids = conn.execute("SELECT CommissionID FROM CommissionInfo").fetchall()
#
#         # Extracting existing CommissionIDs from the result set
#         existing_commission_ids = [row[0] for row in existing_commission_ids]
#
#         # Filter out rows with existing CommissionIDs
#         df_to_insert = df_CommissionInfo[~df_CommissionInfo['CommissionID'].isin(existing_commission_ids)]
#
#         if df_to_insert.empty:
#             print("All CommissionIDs already exist in the database. No new records inserted.")
#             return
#
#         # Insert only the rows with unique CommissionIDs
#         df_to_insert.to_sql('CommissionInfo', con=engine, if_exists='append', index=False,
#                             dtype=sql_dtypes_CommissionInfo)
#         print(f"Inserted {len(df_to_insert)} new records into the CommissionInfo table.")
#
#     finally:
#         # Closing the connection
#         conn.close()


# def Insert_Database(df, table_name, sql_dtypes):
#     # Create the SQLAlchemy engine
#     # Replace 'your_username', 'your_password', 'your_host' and 'your_database' with your actual database credentials
#     engine = create_engine('mssql+pyodbc://your_username:your_password@your_host/your_database')
#
#     # Check if any of the CommissionID values already exist in the database
#     existing_commission_ids = engine.execute(f"SELECT CommissionID FROM {table_name}").fetchall()
#     existing_commission_ids = [row[0] for row in existing_commission_ids]
#
#     # Filter out rows with existing CommissionID values
#     df_to_insert = df[~df['CommissionID'].isin(existing_commission_ids)]
#
#     if len(df_to_insert) == 0:
#         print("No new data to insert. All CommissionID values already exist in the database.")
#         return
#
#     try:
#         # Insert only the rows with new CommissionID values into the database
#         df_to_insert.to_sql(table_name, con=engine, if_exists='append', index=False, dtype=sql_dtypes)
#         print("Data inserted successfully.")
#     except IntegrityError as e:
#         print(f"Error: {e}")

# def Insert_Database(df_CommissionInfo):
#     # Writing the DataFrame to the SQL Server table
#     engine = get_database_engine()
#
#     try:
#         # Establishing a connection
#         conn = engine.connect()
#
#         # Fetching existing CommissionIDs from the database
#         existing_commission_ids = conn.execute("SELECT CommissionID FROM CommissionInfo").fetchall()
#
#         # Extracting existing CommissionIDs from the result set
#         existing_commission_ids = [row[0] for row in existing_commission_ids]
#
#         # Filter out rows with existing CommissionIDs
#         df_to_insert = df_CommissionInfo[~df_CommissionInfo['CommissionID'].isin(existing_commission_ids)]
#
#         if df_to_insert.empty:
#             print("All CommissionIDs already exist in the database. No new records inserted.")
#             return
#
#         # Insert only the rows with unique CommissionIDs
#         df_to_insert.to_sql('CommissionInfo', con=engine, if_exists='append', index=False,
#                             dtype=sql_dtypes_CommissionInfo)
#         print(f"Inserted {len(df_to_insert)} new records into the CommissionInfo table.")
#
#     finally:
#         # Closing the connection
#         conn.close()
# def Insert_Database(df_CommissionInfo):
#     # Writing the DataFrame to the SQL Server table
#
#     engine = get_database_engine()
#     # Establishing a connection
#     conn = engine.connect()
#
#     try:
#         # Fetching existing CommissionIDs from the database
#         existing_commission_ids = conn.execute("SELECT CommissionID FROM CommissionInfo").fetchall()
#
#         # Extracting existing CommissionIDs from the result set
#         existing_commission_ids = [row[0] for row in existing_commission_ids]
#
#         # Filter out rows with existing CommissionIDs
#         df_to_insert = df_CommissionInfo[~df_CommissionInfo['CommissionID'].isin(existing_commission_ids)]
#
#         if df_to_insert.empty:
#             print("All CommissionIDs already exist in the database. No new records inserted.")
#             return
#             # Insert only the rows with unique CommissionIDs
#             df_to_insert.to_sql('CommissionInfo', con=engine, if_exists='append', index=False,
#                                 dtype=sql_dtypes_CommissionInfo)
#             print(f"Inserted {len(df_to_insert)} new records into the CommissionInfo table.")
#
#     finally:
#         # Closing the connection
#         conn.close()

    # Establish a connection
    # with engine.connect() as conn:
    #     # Fetch existing CommissionIDs from the database
    #     existing_commission_ids = conn.execute("SELECT CommissionID FROM CommissionInfo").fetchall()
    #
    # # Convert the result to a list of CommissionIDs
    # existing_commission_ids = [row[0] for row in existing_commission_ids]

    # # Establishing a connection
    # conn = engine.connect()
    #
    # # Fetching existing CommissionIDs from the database
    # existing_commission_ids = conn.execute("SELECT CommissionID FROM CommissionInfo").fetchall()
    #
    # # Closing the connection
    # conn.close()

    # # Check if CommissionID already exists in the database
    # existing_commission_ids = engine.execute("SELECT CommissionID FROM CommissionInfo").fetchall()
    # existing_commission_ids = [row[0] for row in existing_commission_ids]

    # Filter out rows with existing CommissionIDs
    # df_to_insert = df_CommissionInfo[~df_CommissionInfo['CommissionID'].isin(existing_commission_ids)]
    #
    # if df_to_insert.empty:
    #     print("All CommissionIDs already exist in the database. No new records inserted.")
    #     return
    #
    # # Insert only the rows with unique CommissionIDs
    # df_to_insert.to_sql('CommissionInfo', con=engine, if_exists='append', index=False,
    #                     dtype=sql_dtypes_CommissionInfo)
    # print(f"Inserted {len(df_to_insert)} new records into the CommissionInfo table.")


    # df_CommissionInfo.to_sql('CommissionInfo', con=engine, if_exists='append', index=False,
    #                             dtype=sql_dtypes_CommissionInfo)

