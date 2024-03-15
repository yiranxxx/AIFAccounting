import pandas as pd
from PDFextract import extract_pdf
from datetime import datetime

file_path1 = r"D:\Python\AIFAccounting\Feb 5 - Feb 11, 2022.pdf"

# Extract tables using the defined function extract_details
df0, df1, df2 = extract_pdf(file_path1)

table = df0

#table.to_csv('combined_extracted_tables_commision_info.csv', index=True, header=True)

#print("All tables have been concatenated and saved to 'combined_extracted_tables_commision_info.csv'. ")

def convert_table_to_single_row(table):
    # Extracting information from the table
    FileNumber = table.iloc[0, 3]

    report_period_str = table.iloc[2, 1]
    report_period_list = report_period_str.split(' ')

    # Check if there are enough elements in report_period_list
    if len(report_period_list) >= 15:
        # Extracting start and end dates separately
        ReportStartDate_str = ' '.join(report_period_list[5:8])
        ReportEndDate_str = ' '.join(report_period_list[11:])

        try:
            ReportStartDate = datetime.strptime(ReportStartDate_str, '%B %d, %Y').date()
        except ValueError:
            ReportStartDate = None

        try:
            ReportEndDate = datetime.strptime(ReportEndDate_str, '%B %d, %Y').date()
        except ValueError:
            ReportEndDate = None
    else:
        ReportStartDate = None
        ReportEndDate = None

    AdvisorCode_raw = table.iloc[3, 0].split('Code : ')[1].strip()
    AdvisorCode = AdvisorCode_raw.split(' ')[0] + AdvisorCode_raw.split(' ')[1] 

    AdvisorName = table.iloc[4, 0].split('Name : ')[1]

    ContractDateStr = table.iloc[5, 0].split('Contract Date : ')[1].split(' (')[0]
    ContractDate = datetime.strptime(ContractDateStr, '%B %d, %Y').date()

    ContractStatus = table.iloc[5, 0].split('Contract Date : ')[1].split(' (')[1].replace(')', '')

    Agency = table.iloc[3, 3]
    District = table.iloc[4, 3]

    # Create a new DataFrame with a single row
    df_cleaned = pd.DataFrame([[ReportStartDate, ReportEndDate, FileNumber,
                                AdvisorCode, AdvisorName, ContractDate, ContractStatus, Agency, District]],
                              columns=['ReportStartDate', 'ReportEndDate', 'FileNumber',
                                       'AdvisorCode', 'AdvisorName', 'ContractDate', 'ContractStatus',
                                       'Agency', 'District'])

    return df_cleaned

# Assuming you have the original table 'df0'
# You need to replace 'df0' with the actual variable containing your table
# For example, df0 = extract_table_function()

# Call the function to get the cleaned DataFrame
cleaned_dataframe = convert_table_to_single_row(df0)

# Export the cleaned data to a new CSV file
cleaned_file_path = 'cleaned_data.csv'
cleaned_dataframe.to_csv(cleaned_file_path, index=False)

print("Cleaned data has been exported to 'cleaned_data.csv'.")