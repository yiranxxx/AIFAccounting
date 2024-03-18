import pyodbc


def connect_db():
    d = {
        "server": "LAPTOP-9OEFISU5\SQL2019PB",
        "database": "AIF_OLAP_Intern_Test"
    }
    connect_str = 'DRIVER={SQL Server};SERVER=' + d["server"] + ';DATABASE=' + d["database"]
    return pyodbc.connect(connect_str)
