
def insert_data_to_db(connection, t, params):
    cursor = connection.cursor()
    match t:
        case 1:
            sql_insert_query = 'INSERT INTO CommissionInfo (CommissionID, InstitutionName, ReportStartDate, ReportEndDate, FileNumber, AdvisorCode, AdvisorName, ContractDate, ContractStatus, Agency, District) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        case 2:
            sql_insert_query = 'INSERT INTO CommissionDetail (CommissionID, CommissionType, CustomerName, ContractNumber, CoverageName, TransactionDate, TransactionType, CompensationBasisAmount, RPLPer, SharPer, CommPer, AmountDue, Balance) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        case 3:
            sql_insert_query = 'INSERT INTO CommissionPayment (CommissionID, CompanyCode, PayToName, TransactionDate, TransactionType, CommPer, AmountDue, Balance, CurrentBalance) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        case _:
            print ("error")
    cursor.execute(sql_insert_query, params)
    connection.commit()
    cursor.close()