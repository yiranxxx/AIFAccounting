import pandas as pd
from PDFextract import extract_pdf
from datetime import datetime
#
file_path1 = r"D:\Python\AIFAccounting\Feb 5 - Feb 11, 2022.pdf"
#
# Extract tables using the defined function extract_details
df0, df1, df2 = extract_pdf(file_path1)
#
table = df0

# Function to convert DataFrame to single row
def convert_df_to_single_row(df, institution_name):
    # Extracting information from the DataFrame
    FileNumber = df.iloc[0, 3]

    # Extract the string from the specified cell
    report_period_str = str(df.iloc[2, 1])

    # Extract ReportStartDate and ReportEndDate from the report_period_str
    start_index = report_period_str.find('FROM') + len('FROM')
    end_index = report_period_str.find('TO')
    ReportStartDate_str = report_period_str[start_index:end_index].strip()

    start_index = end_index + len('TO')
    ReportEndDate_str = report_period_str[start_index:].strip()

    # Convert ReportStartDate and ReportEndDate to datetime objects
    try:
        ReportStartDate = datetime.strptime(ReportStartDate_str, '%B %d, %Y').date()
    except ValueError:
        ReportStartDate = None

    try:
        ReportEndDate = datetime.strptime(ReportEndDate_str, '%B %d, %Y').date()
    except ValueError:
        ReportEndDate = None

    # Extract the year from the ReportEndDate
    end_date_year = ReportEndDate.year
    print(end_date_year)

    AdvisorCode_raw = df.iloc[3, 0].split('Code : ')[1].strip()
    AdvisorCode = AdvisorCode_raw.split(' ')[0] + AdvisorCode_raw.split(' ')[1]

    # Extract the AdvisorName string from the specified cell
    AdvisorName1 = df.iloc[4, 0].split('Name : ')[1]

    # Split the AdvisorName into first name and last name
    first_name, last_name = AdvisorName1.split()

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

    # Create a new DataFrame with a single row
    df_cleaned = pd.DataFrame([[CommissionID, InstitutionName, ReportStartDate, ReportEndDate, FileNumber, AdvisorCode, AdvisorName, ContractDate, ContractStatus, Agency, District]],
                              columns=['CommissionID', 'InstitutionName', 'ReportStartDate', 'ReportEndDate', 'FileNumber', 'AdvisorCode', 'AdvisorName', 'ContractDate', 'ContractStatus',
                                       'Agency', 'District'])

    return df_cleaned,CommissionID, end_date_year, AdvisorName

## Set the value for InstitutionName
institution_name = 'IA'
#
# Call the function to get the cleaned DataFrame
cleaned_dataframe = convert_df_to_single_row(df0, institution_name)
#
# Export the cleaned data to a new CSV file
cleaned_file_path = 'cleaned_data2.csv'
cleaned_dataframe.to_csv(cleaned_file_path, index=False)
#
print("Cleaned data has been exported to 'cleaned_data2.csv'.")
