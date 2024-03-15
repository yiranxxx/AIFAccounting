import pyodbc

def connect_db():
    d = {
        "server": "192.168.2.86,1433",
        "database": "AIF_OLAP_Test_Intern",
        "port": "1433",
        "username": "OLAP_Intern",
        "password": "1qaz@WSX"
    }
    connect_str = 'DRIVER={SQL Server};SERVER=' + d["server"] + ';DATABASE=' + d["database"] + ';UID=' + d[
        "username"] + ';PWD=' + d["password"]
    return pyodbc.connect(connect_str)