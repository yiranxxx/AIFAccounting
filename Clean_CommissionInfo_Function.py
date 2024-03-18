import pandas as pd
from PDFextract import extract_pdf
from datetime import datetime

# file_path1 = r"D:\Python\AIFAccounting\Jun 26 - July 2, 2021.pdf"
#
# # Extract tables using the defined function extract_details
# df0, df1, df2 = extract_pdf(file_path1)
#
# table = df0

def clean_commissioninfo(df, institution_name):
    # Extracting information from the DataFrame

    FileNumber_col = [value for value in df.iloc[0] if pd.notnull(value) and value != '']
    FileNumber = FileNumber_col[0] if FileNumber_col else None

    report_period_str_col = [value for value in df.iloc[2] if pd.notnull(value) and value != '']
    report_period_str = report_period_str_col[0] if report_period_str_col else None
    report_period_str = str(report_period_str)

    # Extract ReportStartDate and ReportEndDate from the report_period_str
    start_index = report_period_str.find('FROM') + len('FROM') if 'FROM' in report_period_str else None
    end_index = report_period_str.find('TO') if 'TO' in report_period_str else None
    ReportStartDate_str = report_period_str[start_index:end_index].strip() if start_index is not None and end_index is not None else None

    start_index = end_index + len('TO') if end_index is not None else None
    ReportEndDate_str = report_period_str[start_index:].strip() if start_index is not None else None

    # Convert ReportStartDate and ReportEndDate to datetime objects
    try:
        ReportStartDate = datetime.strptime(ReportStartDate_str, '%B %d, %Y').date() if ReportStartDate_str else None
    except ValueError:
        ReportStartDate = None

    try:
        ReportEndDate = datetime.strptime(ReportEndDate_str, '%B %d, %Y').date() if ReportEndDate_str else None
    except ValueError:
        ReportEndDate = None

    # Extract the year from the ReportEndDate
    EndDate_Year = ReportEndDate.year if ReportEndDate else None

    AdvisorCode_raw = df.iloc[3, 0].split('Code : ')[1].strip()
    AdvisorCode = AdvisorCode_raw.split(' ')[0] + AdvisorCode_raw.split(' ')[1]

    # Extract the AdvisorName string from the specified cell
    AdvisorName1 = df.iloc[4, 0].split('Name : ')[1]

    # Split the AdvisorName into first name and last name
    names = AdvisorName1.split()
    first_name = names[0]

    # Join the English name with the first name
    if len(names) > 2:
        first_name += ' ' + ' '.join(names[1:-1])

    last_name = names[-1]  # Use the last element of the list, which will be the last name

    # Concatenate last name and first name with a comma
    AdvisorName = f"{last_name}, {first_name}"

    ContractDateStr = df.iloc[5, 0].split('Contract Date : ')[1].split(' (')[0]
    ContractDate = datetime.strptime(ContractDateStr, '%B %d, %Y').date()

    ContractStatus = df.iloc[5, 0].split('Contract Date : ')[1].split(' (')[1].replace(')', '')

    Agency = df.iloc[3, 3]
    District = df.iloc[4, 3]

    # Add InstitutionName column with the specified value
    InstitutionName = institution_name

    # Generate CommissionID as the concatenation of InstitutionName, ReportEndDate, and AdvisorCode
    CommissionID = f"{InstitutionName}_{ReportEndDate}_{AdvisorCode}"

    # Extract the week number from the ReportEndDate
    WeekNumber = ReportEndDate.isocalendar()[1] if ReportEndDate else None

    # Create a new DataFrame with a single row
    df_cleaned = pd.DataFrame([[CommissionID, InstitutionName, ReportStartDate, ReportEndDate, FileNumber, AdvisorCode, AdvisorName, ContractDate, ContractStatus, Agency, District, WeekNumber]],
                              columns=['CommissionID', 'InstitutionName', 'ReportStartDate', 'ReportEndDate', 'FileNumber', 'AdvisorCode', 'AdvisorName', 'ContractDate', 'ContractStatus',
                                       'Agency', 'District', 'WeekNumber'])

    # Data type conversions
    # Convert all columns to strings
    # df_cleaned['CommissionID'] = df_cleaned['CommissionID'].astype(str)
    # df_cleaned['InstitutionName'] = df_cleaned['InstitutionName'].astype(str)
    # df_cleaned['FileNumber'] = df_cleaned['FileNumber'].astype(str)
    # df_cleaned['AdvisorCode'] = df_cleaned['AdvisorCode'].astype(str)
    # df_cleaned['AdvisorName'] = df_cleaned['AdvisorName'].astype(str)
    # df_cleaned['ContractStatus'] = df_cleaned['ContractStatus'].astype(str)
    # df_cleaned['Agency'] = df_cleaned['Agency'].astype(str)
    # df_cleaned['District'] = df_cleaned['District'].astype(str)
    #
    # # Convert ContractDate, ReportStartDate and ReportEndDate to datetime
    # df_cleaned['ReportStartDate'] = pd.to_datetime(df_cleaned['ReportStartDate'])
    # df_cleaned['ReportEndDate'] = pd.to_datetime(df_cleaned['ReportEndDate'])
    # df_cleaned['ContractDate'] = pd.to_datetime(df_cleaned['ContractDate'])
    #
    # # Convert WeekNumber to integer
    # df_cleaned['WeekNumber'] = df_cleaned['WeekNumber'].astype(int)

    # return df_cleaned, CommissionID, EndDate_Year, AdvisorName, WeekNumber
    return df_cleaned

# # Set the value for InstitutionName
# institution_name = 'IA'
#
# # Call the function to get the cleaned DataFrame
# cleaned_dataframe = clean_commissioninfo(df0, institution_name)


