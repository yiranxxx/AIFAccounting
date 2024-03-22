from Clean_CommissionInfo_Function import clean_commissioninfo
from Clean_PaymentData_Function import Clean_Payment
from Extract_pdf_function import Extract_PDF
from Public.Find_Pdf_In_Institution_Folder_Function import find_pdf_in_institution_folder
from Public.Write_Log_Function import write_log
from dbutilities.Database_Function import Insert_DB
import pandas as pd


# Setup a DataFrame for logging
log_columns = ['Timestamp', 'File_Path', 'Message', 'Flag']
log_df = pd.DataFrame(columns=log_columns)
log_file_path = r"D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\IA original\process_log.xlsx"




directory_path = r"D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\IA original"

InstitutionName = "iA"


pdf_files = find_pdf_in_institution_folder(directory_path, InstitutionName)

for pdf_file in pdf_files:
    print(pdf_file)
    try:
        df0, df1, df2 = Extract_PDF(pdf_file)
        # CommissionInfo_df,CommissionID, EndDate_Year, AdvisorName, WeekNumber = clean_commissioninfo (df0,InstitutionName)
        CommissionID = "4444444"
        PaymentData_df = Clean_Payment(df1, df2, CommissionID )
        print("Extract Success")

        try:
            Insert_DB(PaymentData_df)
            log_df = write_log (pdf_file, "Data insertion successful", log_df, 'S')
            print("Success")
        except Exception as e:
            log_df = write_log(pdf_file, f"Error inserting data into database: {e}", log_df, 'F')
            print("Insert Failure")
    except Exception as e:
        log_df = write_log (pdf_file, f"Error extracting or cleaning data: {e}", log_df, 'F')
        print("Extract Failure")


# Save the log DataFrame to an Excel file


log_file_path = r"D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\IA original\process_log.xlsx"

# Attempt to load the existing log file
try:
    log_df_old = pd.read_excel(log_file_path)
except FileNotFoundError:
    print(f"File not found: {log_file_path}")
    # Initialize an empty DataFrame with columns if the file does not exist
    log_df_old = pd.DataFrame(columns=['Timestamp', 'File_Path', 'Message', 'Flag'])
except Exception as e:
    print(f"An error occurred: {e}")
    # Initialize an empty DataFrame as a fallback
    log_df_old = pd.DataFrame(columns=['Timestamp', 'File_Path', 'Message', 'Flag'])

# Assuming log_df is defined and contains new log entries
# Append new log entries to the existing ones
combined_log_df = pd.concat([log_df_old, log_df], ignore_index=True)

# Save the combined DataFrame back to the Excel file
combined_log_df.to_excel(log_file_path, index=False)

log_df.to_excel(log_file_path, index=False)