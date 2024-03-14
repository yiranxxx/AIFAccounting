from sqlalchemy.types import String, Date, Numeric

# Explicitly defining SQL data types for each column
sql_dtypes_CommissionDetail = {
    'CommissionID': String(255),
    'CustomerName': String(255),
    'ContractNumber': String(255),
    'CoverageName': String(255),
    'TransactionDate': Date,
    'TransactionType': String(255),
    'CompensationBasisAmount': Numeric(precision=19, scale=4),
    'RPLPer': Numeric(precision=10, scale=2),
    'SharPer': Numeric(precision=10, scale=2),
    'CommPer': Numeric(precision=10, scale=2),
    'AmountDue': Numeric(precision=19, scale=4),
    'Balance': Numeric(precision=19, scale=4),
    'CommissionType': String(255)
}
