import os
from sqlalchemy import create_engine


def get_database_engine():
    defile_dir = r"D:\Python\AIFAccounting\dbutilities"
    try:
        with open(os.path.join(defile_dir, 'dbProperties.properties')) as properties:
            l = [line.split("=") for line in properties.readlines()]
            d = {key.strip(): value.strip() for key, value in l}

        required_keys = ["server", "database"]
        for key in required_keys:
            if key not in d:
                raise Exception(f"Property {key} not found in dbProperties.properties")

        # Set defaults for optional keys
        d.setdefault("port", None)
        d.setdefault("user", None)
        d.setdefault("password", None)

    except Exception as e:
        print(e)
        exit()
    else:
        print("Property file load successful!")

    engine = create_engine(
        f'mssql+pyodbc://{d["user"]}:{d["password"]}@{d["server"]}/{d["database"]}?driver=ODBC+Driver+17+for+SQL+Server')
    return engine
