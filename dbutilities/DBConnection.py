from sqlalchemy import create_engine

def Get_DB_Engine():
    """
    Connects to SQL Server using Windows Authentication and returns the engine object.

    Returns:
        sqlalchemy.engine.base.Engine: The engine object for the SQL Server connection.
    """
    # Define the server name and database name
    server_name = 'DESKTOP-ISM7FG7'
    database_name = 'AIF_Accounting_test'

    # Define the connection string
    connection_string = f'mssql+pyodbc://{server_name}/{database_name}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'

    # Create the engine
    engine = create_engine(connection_string)

    return engine

# Call the function to get the engine object
# engine = connect_to_DB()
# print(engine)

# Now you can use the 'engine' object to interact with your SQL Server database
