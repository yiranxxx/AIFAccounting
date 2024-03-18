from sqlalchemy.types import String, Date, Numeric, Integer

# Explicitly defining SQL data types for each column
sql_dtypes_CommissionInfo = {
    'CommissionID': String(255),
    'InstitutionName': String(255),
    'ReportStartDate': Date,
    'ReportEndDate': Date,
    'FileNumber': String(255),
    'AdvisorCode': String(255),
    'AdvisorName': String(255),
    'ContractDate': Date,
    'ContractStatus': String(255),
    'Agency': String(255),
    'District': String(255),
    'WeekNumber': Integer
}

# Explicitly defining SQL data types for each column
sql_dtypes_CommissionPayment = {
    'CommissionID': String(255),
    'CompanyCode': String(255),
    'PayToName': String(255),
    'TransactionDate': Date,
    'TransactionType': String(255),
    'CommPer': Numeric(precision=10, scale=2),
    'AmountDue': Numeric(precision=19, scale=4),
    'Balance': Numeric(precision=19, scale=4),
    'CurrentBalance': Numeric(precision=19, scale=4)
}