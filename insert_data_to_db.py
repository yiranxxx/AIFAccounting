
def insert_data_to_db(connection, params):
    cursor = connection.cursor()
    sql_insert_query = """INSERT INTO Accounting_TransferFromAffiliated (ReportID,BankNumber, InsuredName, TransactionDate, TransactionType, CommissionPer, AmountDue, Balance,TimeStamp) VALUES (?, ?, ?, ?, ?, ?, ?,?,?)"""
    cursor.execute(sql_insert_query, params)
    connection.commit()
    cursor.close()