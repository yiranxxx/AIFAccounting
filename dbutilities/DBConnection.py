import os
import pyodbc
from sqlalchemy import create_engine


# def get_database_engine():
#     defile_dir = r"D:\AIF(Lisa)\github\AIFAccounting\dbutilities"
#     try:
#         with open(os.path.join(defile_dir, 'dbProperties.properties')) as properties:
#             l = [line.split("=") for line in properties.readlines()]
#             d = {key.strip(): value.strip() for key, value in l}
#
#         required_keys = ["server", "database"]
#         for key in required_keys:
#             if key not in d:
#                 raise Exception(f"Property {key} not found in dbProperties.properties")
#
#         # Set defaults for optional keys
#         d.setdefault("port", None)
#         d.setdefault("user", None)
#         d.setdefault("password", None)
#
#     except Exception as e:
#         print(e)
#         exit()
#     else:
#         print("Property file load successful!")
#
#     engine = create_engine(
#         f'mssql+pyodbc://{d["user"]}:{d["password"]}@{d["server"]}/{d["database"]}?driver=ODBC+Driver+17+for+SQL+Server')
#     return engine


import os
import pyodbc
from sqlalchemy import create_engine

def connect_db():
    defile_dir = r"D:\AIF(Lisa)\github\AIFAccounting\dbutilities"
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




# def connect_db(port=None, user=None, password=None):
#     defile_dir = r"D:\Python\AIFAccounting\dbutilities"
#     try:
#         with open(os.path.join(os.path.dirname(__file__), 'dbProperties.properties')) as properties:
#             l = [line.split("=") for line in properties.readlines()]
#             d = {key.strip(): value.strip() for key, value in l}
#         if "server" not in d or "database" not in d:
#             raise Exception("Property server or database not found")
#         if "port" not in d or "user" not in d or "password" not in d:
#             d["port"] = None
#             d["user"] = None
#             d["password"] = None
#     except Exception as e:
#         print(e)
#         exit()
#     else:
#         print("Property file load successful!")
#
#     connect_str = 'DRIVER={SQL Server};SERVER=' + d["server"] + ';DATABASE=' + d["database"] + ';UID=' + d["user"] + ';PWD=' + d["password"]
#     return pyodbc.connect(connect_str)



# def connect_db():
#     d = {
#         "server": "192.168.2.86,1433",
#         "database": "AIF_Test",
#         "port": "1433",
#         "username": "AccountingTest",
#         "password": "1234qwer"
#     }
#     connect_str = 'DRIVER={SQL Server};SERVER=' + d["server"] + ';DATABASE=' + d["database"] + ';UID=' + d["username"] + ';PWD=' + d["password"]
#     return pyodbc.connect(connect_str)


