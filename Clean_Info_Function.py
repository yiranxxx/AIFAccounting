import pandas as pd
from datetime import datetime


def Extract_Contract_Info(df):
    ContractDate = None
    ContractStatus = None
    Agency = None
    District = None

    for i in range(len(df.index)):
        row_data = df.iloc[i, 0]
        if 'Contract Date :' in row_data:
            ContractDateStr = row_data.split('Contract Date : ')[1].split(' (')[0]
            ContractDate = ContractDateStr

            ContractStatus = row_data.split('Contract Date : ')[1].split(' (')[1].replace(')', '')
        elif 'Agency :' in row_data:
            Agency = row_data.split('Agency : ')[1]
        elif 'District :' in row_data:
            District = row_data.split('District : ')[1]

    return ContractDate, ContractStatus, Agency, District
def Clean_Info(df, Institution_Name):
    FileNumber_col = [value for value in df.iloc[0] if pd.notnull(value) and value != '']
    FileNumber = FileNumber_col[0] if FileNumber_col else None

    report_period_str_col = [value for value in df.iloc[2] if pd.notnull(value) and value != '']
    report_period_str = report_period_str_col[0] if report_period_str_col else None
    report_period_str = str(report_period_str)
    print(report_period_str)

    # Extract ReportStartDate and ReportEndDate from the report_period_str
    start_index = report_period_str.find('FROM') + len('FROM') if 'FROM' in report_period_str else None
    end_index = report_period_str.find(' TO ') if ' TO ' in report_period_str else None
    ReportStartDate_str = report_period_str[
                          start_index:end_index].strip() if start_index is not None and end_index is not None else None

    start_index = end_index + len(' TO ') if end_index is not None else None
    ReportEndDate_str = report_period_str[start_index:].strip() if start_index is not None else None
    print(ReportStartDate_str)
    print(ReportEndDate_str)

    # Convert ReportStartDate and ReportEndDate to datetime objects
    try:
        # ReportStartDate = datetime.strptime(ReportStartDate_str, '%B %d, %Y').date() if ReportStartDate_str else None
        ReportStartDate = ReportStartDate_str if ReportStartDate_str else None
    except ValueError:
        ReportStartDate = None

    try:
        # ReportEndDate = datetime.strptime(ReportEndDate_str, '%B %d, %Y').date() if ReportEndDate_str else None
        ReportEndDate = ReportEndDate_str if ReportEndDate_str else None
    except ValueError:
        ReportEndDate = None

    ReportEndDate2 = datetime.strptime(ReportEndDate_str, '%B %d, %Y').date() if ReportEndDate_str else None
    End_Date_Year = ReportEndDate2.year if ReportEndDate else None

    AdvisorCode_raw = df.iloc[3, 0].split('Code : ')[1].strip()

    # Split the AdvisorCode_raw and concatenate the parts if available
    split_parts = AdvisorCode_raw.split(' ')
    if len(split_parts) >= 1:
        AdvisorCode = split_parts[0]
        if len(split_parts) > 1:
            AdvisorCode += split_parts[1]
    else:
        AdvisorCode = None

    # Extract the AdvisorName string from the specified cell
    AdvisorName1 = df.iloc[4, 0].split('Name : ')[1]

    # Check if the name is the company name
    if AdvisorName1 == "AI FINANCIAL POWER GROUP LIMITED":
        AdvisorName = AdvisorName1  # It's a company name, keep it unchanged
    else:
        # Split the AdvisorName into first name and last name
        names = AdvisorName1.split()
        first_name = names[0]

        # Join the English name with the first name
        if len(names) > 2:
            first_name += ' ' + ' '.join(names[1:-1])

        last_name = names[-1]  # Use the last element of the list, which will be the last name

        # Concatenate last name and first name with a comma
        AdvisorName = f"{last_name}, {first_name}"

    # Extract contract information
    ContractDate, ContractStatus, Agency, District = Extract_Contract_Info(df)

    # Add InstitutionName column with the specified value
    InstitutionName = Institution_Name

    # Generate CommissionID as the concatenation of InstitutionName, ReportEndDate, and AdvisorCode
    CommissionID = f"{InstitutionName}_{ReportEndDate}_{AdvisorCode}"

    # Extract the week number from the ReportEndDate
    WeekNumber = ReportEndDate2.isocalendar()[1] if ReportEndDate else None

    # Create a new DataFrame with a single row
    df_cleaned = pd.DataFrame([[CommissionID, InstitutionName, ReportStartDate, ReportEndDate, FileNumber, AdvisorCode,
                                AdvisorName, ContractDate, ContractStatus, Agency, District, WeekNumber]],
                              columns=['CommissionID', 'InstitutionName', 'ReportStartDate', 'ReportEndDate',
                                       'FileNumber', 'AdvisorCode', 'AdvisorName', 'ContractDate', 'ContractStatus',
                                       'Agency', 'District', 'WeekNumber'])

    return df_cleaned, CommissionID, End_Date_Year, AdvisorName, WeekNumber, ReportStartDate, ReportEndDate

