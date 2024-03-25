import pandas as pd
import re
from PDFextract import extract_pdf
from datetime import datetime

df0, df1, df2 = extract_pdf(file_path1)

def Extract_Contract_Info(df):
    ContractDate = None
    ContractStatus = None

    for i in range(len(df.index)):
        row_data = df.iloc[i, 0]
        if 'Contract Date :' in row_data:
            ContractDate = row_data.split('Contract Date : ')[1].split(' (')[0]
            ContractStatus = row_data.split('Contract Date : ')[1].split(' (')[1].replace(')', '')
            break
    return ContractDate, ContractStatus

def Extract_Agency_District(df):
    Agency = None
    District = None

    if len(df.index) > 4 and len(df.columns) > 3:
        if pd.notnull(df.iloc[3, 3]):
            Agency = df.iloc[3, 3]
        if pd.notnull(df.iloc[4, 3]):
            District = df.iloc[4, 3]

    return Agency, District

def Clean_Info(df, institution_name):

    FileNumber_col = [value for value in df.iloc[0] if pd.notnull(value) and value != '']
    FileNumber = FileNumber_col[0] if FileNumber_col else None

    report_period_str_col = [value for value in df.iloc[2] if pd.notnull(value) and value != '']
    report_period_str = report_period_str_col[0] if report_period_str_col else None
    report_period_str = str(report_period_str)

    # Extract ReportStartDate and ReportEndDate from the report_period_str
    start_index = report_period_str.find('FROM') + len('FROM') if 'FROM' in report_period_str else None
    end_index = report_period_str.find(' TO ') if re.search(r'\bTO\b', report_period_str) else None
    ReportStartDate = report_period_str[
                          start_index:end_index].strip() if start_index is not None and end_index is not None else None

    start_index = end_index + len('TO') if end_index is not None else None
    ReportEndDate = report_period_str[end_index + len(' TO '):].strip() if end_index is not None else None

    # Convert ReportStartDate and ReportEndDate to datetime objects
    try:
        ReportStartDate_Transfer = datetime.strptime(ReportStartDate, '%B %d, %Y').date() if ReportStartDate else None
    except ValueError:
        ReportStartDate_Transfer = None

    try:
        ReportEndDate_Transfer = datetime.strptime(ReportEndDate, '%B %d, %Y').date() if ReportEndDate else None
    except ValueError:
        ReportEndDate_Transfer = None

    # Extract the year from the ReportEndDate
    EndDate_Year = ReportEndDate_Transfer.year if ReportEndDate_Transfer else None

    AdvisorCode_raw = df.iloc[3, 0].split('Code : ')[1].strip()
    split_parts = AdvisorCode_raw.split(' ')
    if len(split_parts) >= 1:
        AdvisorCode = split_parts[0]
        if len(split_parts) > 1:
            AdvisorCode += split_parts[1]
    else:
        AdvisorCode = None

    # Extract the AdvisorName string from the specified cell
    AdvisorName1 = df.iloc[4, 0].split('Name : ')[1]
    if AdvisorName1 == "AI FINANCIAL POWER GROUP LIMITED":
        AdvisorName = AdvisorName1
    else:
        names = AdvisorName1.split()
        first_name = names[0]

        if len(names) > 2:
            first_name += ' ' + ' '.join(names[1:-1])
        last_name = names[-1]

        AdvisorName = f"{last_name}, {first_name}"

    ContractDate, ContractStatus = Extract_Contract_Info(df)
    Agency, District = Extract_Agency_District(df)

    # Add InstitutionName column with the specified value
    InstitutionName = institution_name

    # Generate CommissionID as the concatenation of InstitutionName, ReportEndDate, and AdvisorCode
    CommissionID = f"{InstitutionName}_{ReportEndDate}_{AdvisorCode}"

    # Extract the week number from the ReportEndDate
    WeekNumber = ReportEndDate_Transfer.isocalendar()[1] if ReportEndDate_Transfer else None

    # Create a new DataFrame with a single row
    df_info = pd.DataFrame([[CommissionID, InstitutionName, ReportStartDate, ReportEndDate, FileNumber, AdvisorCode,
                                AdvisorName, ContractDate, ContractStatus, Agency, District, WeekNumber]],
                              columns=['CommissionID', 'InstitutionName', 'ReportStartDate', 'ReportEndDate',
                                       'FileNumber', 'AdvisorCode', 'AdvisorName', 'ContractDate', 'ContractStatus',
                                       'Agency', 'District', 'WeekNumber'])

    return df_info,CommissionID, EndDate_Year, AdvisorName, WeekNumber, ReportStartDate, ReportEndDate

# Set the value for InstitutionName
institution_name = 'IA'

# Call the function to get the cleaned DataFrame
cleaned_dataframe = Clean_Info(df0, institution_name)


