from DBConnection import connect_db
from Extract_wholeData_from_pdf import extract_wholetext_from_pdf
from insert_data_to_db import insert_data_to_db
from LoopExtractData import split_transfer_data

pdf_path = r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\Jun 26 - July 2, 2021 - Mock.pdf'


db_connection = connect_db()


content = extract_wholetext_from_pdf(pdf_path)
params_transfer = split_transfer_data(content)  # Ensure this function returns data in the correct order and format


if params_transfer :
    insert_data_to_db(db_connection, params_transfer )
    print("Data inserted successfully.")
else:
    print("No data to insert.")
