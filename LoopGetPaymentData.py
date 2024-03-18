

from Clean_PaymentData_Function0312 import clean_payment
from Extract_pdf_function import extract_pdf
from Public.Find_Pdf_In_Institution_Folder_Function import find_pdf_in_institution_folder
from dbutilities.Insert_Database_Function import Insert_Database


directory_path = r"D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\IA original"

InstitutionName ="iA"
pdf_files = find_pdf_in_institution_folder(directory_path, InstitutionName)


# Loop through each PDF file and extract tables
for pdf_file in pdf_files:

    # Get the full file path
    # Extract tables using the defined function extract_details
    df0, df1, df2 = extract_pdf(pdf_file)

    PaymentData_df = clean_payment(df1, df2, 'AAAAAA')
    Insert_Database(PaymentData_df)
    # write log file




    # copy  file to specific folder

    print("Extract Successful!")
    print(pdf_file)


