from sqlalchemy.types import String, Date, Numeric

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