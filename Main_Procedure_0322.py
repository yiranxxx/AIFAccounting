import pandas as pd
import glob
import os

from Extract_PDF_Function import Extract_PDF
from Clean_Info_Function import Clean_Info
from Clean_Detail_Function import Clean_Detail
from Clean_Payment_Function import Clean_Payment
from Public.Detect_PDF_Files_Function import Detect_PDF
from Public.Manipulate_PDF_Files_Function import Move_PDF, Copy_PDF
from dbutilities.Database_Function import Insert_DB, Check_Commission_Id_Exists
from Public.Write_Log_Function import Write_Log

'''
Path to be modified:
Main_Procedure: log_file_path, directory_path
Manipulate_PDF_File_Function: destination_folder
DBConnection: defile_dir
'''

# Setup a DataFrame for logging
log_columns = ['Timestamp', 'File_Path', 'Message', 'Flag']
log_df = pd.DataFrame(columns=log_columns)
log_file_path = r"D:\AccountingProject\Logfile\process_log.xlsx"

# # read pdf files
# directory_path = r"\\AIF-NAS01\AI_Financial\Admin\Accounting\Commission"
# Institution_Name = "iA"
# pdf_files = Detect_PDF(directory_path, Institution_Name)


file_name = r"D:\AccountingProject\Logfile\Errorlist.xlsx"

# Read the Excel file into a DataFrame
error_df = pd.read_excel(file_name)

# Assuming you want to extract the second column, which is indexed as 1
# If you know the column name, it's better to use it directly, e.g., error_df['ColumnName']
pdf_files = error_df['File_Path'].tolist()

# pdf_files = [r'\\AIF-NAS01\AI_Financial\Admin\Accounting\Commission\AIF\iA\2021\Aug 21 - Aug 27, 2021.pdf', r'\\AIF-NAS01\AI_Financial\Admin\Accounting\Commission\AIF\iA\2021\Aug 28 - Sep 3, 2021.pdf']

# Print the extracted column values
for file in pdf_files:
    try:
        # Extract contents from pdf file
        df0, df1, df2 = Extract_PDF(file)
        try:
            if df0 is None and df1 is None and df2 is None:
                print("Skip file with 2 pages")
                continue

            # Clean data
            df_info, CommissionID, EndDate_Year, AdvisorName, WeekNumber, StartDate, EndDate = Clean_Info(df0,
                                                                                                          Institution_Name)
            df_detail = Clean_Detail(df1, df2, CommissionID)
            df_payment = Clean_Payment(df1, df2, CommissionID)

            # if Check_Commission_Id_Exists(CommissionID):
            #     log_df = Write_Log(file, "CommissionID is already exist in database!", log_df, 'D')
            # else:

            try:
                # Insert data into SQL db
                Insert_DB(df_info, df_detail, df_payment)

                print("Success")
                # Move extracted pdf to history folder
                # Move_PDF(file, AdvisorName, Institution_Name, EndDate_Year, WeekNumber, StartDate, EndDate)
                # Copy extracted pdf to history folder
                # Copy_PDF(file, AdvisorName, Institution_Name, EndDate_Year, WeekNumber, StartDate, EndDate)

                log_df = Write_Log(file, "Data insertion successful", log_df, 'S')

            except Exception as e:
                log_df = Write_Log(file, f"Error inserting data into database: {e}", log_df, 'F')
                print("Failure")
        except Exception as e:
            log_df = Write_Log(file, f"Error cleaning data: {e}", log_df, 'F')
            print("Clean Data Error")
    except Exception as e:
        log_df = Write_Log(file, f"Error extracting data: {e}", log_df, 'F')
        print("Extract Data Error")
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
