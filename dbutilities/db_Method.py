from dbutilities import DBConnection, dbColumns


# def parameter_commastring(columns):
#     """
#         This method returns a string that contains a comma-separated list of question marks,
#         with each question mark representing a parameter in the columns list.
#         :param columns: A list of column names.
#         :return: A string that contains a comma-separated list of question marks,
#                  with each question mark representing a parameter in the columns list.
#     """
#     return '?, ' * (len(columns) -1)
def Insert_CommissionPayment(engine,df):
    """
        This method is used to insert multiple rows of data into the "Client_Current" table in a database.
        :param cursor: A cursor object that allows interaction with the database.
        :param values: A list of tuples, where each tuple represents a row of data to be inserted into
                       the "Client_Current" table.
        :return: Nothing return. It inserts the rows of data into the "Client_Current" table in the database.
        """


    # sql = "INSERT INTO CommissionPayment VALUES ( "  +parameter_commastring(dbColumns.CommissionPayment_columns) + "getdate())"
    #
    # # Using executemany to insert data. If you have only one set of data, you can use execute instead.
    # cursor.executemany(sql, values )
    #
    # # Commit the transaction to make the changes persistent in the database.
    # cursor.commit()
    df.to_sql('CommissionPayment', con=engine, if_exists='append', index=False)
