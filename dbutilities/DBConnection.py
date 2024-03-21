import os
from sqlalchemy import create_engine
import pyodbc

def connect_db():
    defile_dir = r"D:\AIF Intern\Accounting\PyCharmProjects\AIF Intern"
    try:
        with open(os.path.join(defile_dir, 'dbProperties.properties')) as properties:
            properties_dict = {key.strip(): value.strip() for key, value in (line.split("=") for line in properties if line.strip())}

        for key in ["server", "database"]:
            if key not in properties_dict:
                raise ValueError(f"Property {key} not found in dbProperties.properties")

        # Set defaults for optional keys
        properties_dict.setdefault("port", "1433")  # Default SQL Server port
        properties_dict.setdefault("user", "sa")  # Default user (adjust as needed)
        properties_dict.setdefault("password", "")  # Default password (adjust as needed)

    except Exception as e:
        raise Exception(f"Error reading properties file: {e}")

    sqlalchemy_engine = create_engine(
        f"mssql+pyodbc://{properties_dict['user']}:{properties_dict['password']}@{properties_dict['server']}/{properties_dict['database']}?driver=ODBC+Driver+17+for+SQL+Server"
    )
    pyodbc_connection_string = f"DRIVER={{SQL Server}};SERVER={properties_dict['server']};DATABASE={properties_dict['database']};UID={properties_dict['user']};PWD={properties_dict['password']}"
    pyodbc_connection = pyodbc.connect(pyodbc_connection_string)

    return sqlalchemy_engine, pyodbc_connection


