from dbutilities.DBConnection import connect_db
from dbutilities.DBColumnsType import sql_dtypes_CommissionInfo, sql_dtypes_CommissionPayment, sql_dtypes_CommissionDetail
from dbutilities.DBConnection_Local import connect_db
def Insert_DB (df_info, df_detail, df_payment):

    #engine,_ = connect_db()
    engine = connect_db()

    if df_detail is not None:

        df_info.to_sql('CommissionInfo', con=engine, if_exists='append', index=False,
                       dtype=sql_dtypes_CommissionInfo)

        df_detail.to_sql('CommissionDetail', con=engine, if_exists='append', index=False,
                         dtype=sql_dtypes_CommissionDetail)

        df_payment.to_sql('CommissionPayment', con=engine, if_exists='append', index=False,
                          dtype=sql_dtypes_CommissionPayment)
    else:
        df_info.to_sql('CommissionInfo', con=engine, if_exists='append', index=False,
                       dtype=sql_dtypes_CommissionInfo)

        df_payment.to_sql('CommissionPayment', con=engine, if_exists='append', index=False,
                          dtype=sql_dtypes_CommissionPayment)

    print('Data inserted successfully')

def Check_Commission_Id_Exists(commission_id):
    engine, connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM CommissionInfo WHERE CommissionID = ?', (commission_id,))
    count = cursor.fetchone()[0]
    return count > 0