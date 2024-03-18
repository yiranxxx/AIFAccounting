from dbutilities.DBConnection import get_database_engine
from dbutilities.dbColumnsType import sql_dtypes_CommissionPayment


# For SQL Server Authentication
def Insert_Database(df_CommissionPayment):
    # Writing the DataFrame to the SQL Server table

    engine = get_database_engine()
    df_CommissionPayment.to_sql('CommissionPayment', con=engine, if_exists='append', index=False,
                                dtype=sql_dtypes_CommissionPayment)
