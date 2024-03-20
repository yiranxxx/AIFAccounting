from dbutilities.DBConnection import connect_db
from dbutilities.dbColumnsType import sql_dtypes_CommissionPayment


# For SQL Server Authentication
def Insert_Database(engine,df_CommissionPayment):

    df_CommissionPayment.to_sql('CommissionPayment', con=engine, if_exists='append', index=False,
                                dtype=sql_dtypes_CommissionPayment)



def check_commission_id_exists(db_connection, commission_id):
    cursor = db_connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM CommissionInfo WHERE CommissionID = ?', (commission_id,))
    count = cursor.fetchone()[0]
    return count > 0





# engine, connection = connect_db()
# commission_id_to_check = 'IA_2021-07-02_290327(000)'
# exists = check_commission_id_exists(connection, commission_id_to_check)
# print(exists)







# # Assuming connect_db is correctly defined elsewhere and returns a database connection
#     # Assuming connect_db is correctly defined elsewhere and returns both an engine and a pyodbc connection
#     engine, connection = connect_db()
#
#     # No need to call connection.cursor() if using a context manager with pyodbc's connection object
#     with connection:
#         with connection.cursor() as cursor:
#             # Define the parameters as a tuple
#             params = ('s2121', 'fwf', 'AI FINANCIAL POWER G', '2022-02-11', 'Transfer XFR', 0, -84, 84, 84)
#
#             # SQL insert query
#             sql_insert_query = """INSERT INTO CommissionPayment (CommissionID, CompanyCode, PayToName, TransactionDate, TransactionType, CommPer, AmountDue, Balance, CurrentBalance) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
#
#             # Execute the query
#             cursor.execute(sql_insert_query, params)
#
#             # Commit the transaction
#             connection.commit()
