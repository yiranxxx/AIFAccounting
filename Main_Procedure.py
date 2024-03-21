import pandas as pd
import glob
import os

from Extract_PDF_Function import Extract_PDF
from Clean_Info_Function import Clean_Info
from Clean_Detail_Function import Clean_Detail
from Clean_Payment_Function import Clean_Payment
from Public.Detect_PDF_Files_Function import Detect_PDF
from Public.Manipulate_PDF_Files_Function import Move_PDF,Copy_PDF
from dbutilities.Database_Function import Insert_DB,Check_Commission_Id_Exists
from Public.Write_Log_Function import Write_Log

# Path to be modified:
# Main_Procedure: log_file_path, directory_path
# Manipulate_PDF_File_Function: destination_folder
# DBConnection: defile_dir

# Setup a DataFrame for logging
log_columns = ['Timestamp', 'File_Path', 'Message', 'Flag']
log_df = pd.DataFrame(columns=log_columns)
log_file_path = r"D:\AIF Intern\Accounting\Commission\process_log.xlsx"


# # read pdf files
# directory_path = r"D:\AIF Intern\Accounting\Commission\OriginalFile"
Institution_Name = "iA"
# pdf_files = Detect_PDF(directory_path, Institution_Name)

directory_path = r"\\192.168.2.8\AIF_Interns\202312\Accounting\ErrorFile\test"


# Change the working directory to the specified path
os.chdir(directory_path)

# Find all PDF files in the directory and its subdirectories
pdf_files = glob.glob('**/*.pdf', recursive=True)
for file in pdf_files:
    try:
        # Extract contents from pdf file
        df0, df1, df2 = Extract_PDF(file)
        if df0 is None and df1 is None and df2 is None:
            print("Skip file with 2 pages")
            continue

        # Clean data
        df_info, CommissionID, EndDate_Year, AdvisorName, WeekNumber, StartDate, EndDate = Clean_Info(df0, Institution_Name)
        df_detail = Clean_Detail(df1, df2, CommissionID)
        df_payment = Clean_Payment(df1, df2, CommissionID)
        if Check_Commission_Id_Exists(CommissionID):
            log_df = Write_Log(file, "CommissionID is already exist in database!", log_df, 'D')
        else:

            try:
                # Insert data into SQL db
                Insert_DB(df_info, df_detail, df_payment)

                print("Success")
                # Move extracted pdf to history folder
                # Move_PDF(file, AdvisorName, Institution_Name, EndDate_Year, WeekNumber, StartDate, EndDate)
                # Copy extracted pdf to history folder
                Copy_PDF(file, AdvisorName, Institution_Name, EndDate_Year, WeekNumber, StartDate, EndDate)

                log_df = Write_Log(file, "Data insertion successful", log_df, 'S')

            except Exception as e:
                log_df = Write_Log(file, f"Error inserting data into database: {e}", log_df, 'F')
                print("Failure")
    except Exception as e:
        log_df = Write_Log (file, f"Error extracting or cleaning data: {e}", log_df, 'F')

# Save the log DataFrame to an Excel file
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

# log_df.to_excel(log_file_path, index=False)





