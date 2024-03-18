from dbutilities.DBConnection import Get_DB_Engine
from dbutilities.DBColumnsType import sql_dtypes_CommissionInfo, sql_dtypes_CommissionPayment, sql_dtypes_CommissionDetail

def Insert_DB (df_info, df_detail, df_payment):

    engine = Get_DB_Engine()

    df_info.to_sql('CommissionInfo', con=engine, if_exists='append', index=False,
                   dtype=sql_dtypes_CommissionInfo)

    df_detail.to_sql('CommissionDetail', con=engine, if_exists='append', index=False,
                     dtype=sql_dtypes_CommissionDetail)

    df_payment.to_sql('CommissionPayment', con=engine, if_exists='append', index=False,
                      dtype=sql_dtypes_CommissionPayment)