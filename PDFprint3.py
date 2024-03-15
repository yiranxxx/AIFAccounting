import pandas as pd
from datetime import datetime

# Load the CSV file into a DataFrame
df = pd.read_csv('combined_extracted_tables_commision_info.csv')

# Extract the string from the specified cell and convert it to a string
report_period_str = str(df.iloc[2, 2])


# Print the report period string for inspection
print("Report Period String:", report_period_str)

# Check if the report period string is not null or empty
if report_period_str.strip().lower() != 'nan':

    # Check if 'FROM' and 'TO' are present in the report period string
    if 'FROM' in report_period_str and 'TO' in report_period_str:
        # Extract ReportStartDate and ReportEndDate
        start_index = report_period_str.find('FROM') + len('FROM')
        end_index = report_period_str.find('TO')

        # Check if start and end indices are valid
        if start_index != -1 and end_index != -1 and start_index < end_index:
            ReportStartDate_str = report_period_str[start_index:end_index].strip()
            ReportEndDate_str = report_period_str[end_index + len('TO'):].strip()

            # Convert ReportStartDate and ReportEndDate to datetime objects
            try:
                ReportStartDate = datetime.strptime(ReportStartDate_str, '%B %d, %Y').date()
            except ValueError:
                ReportStartDate = None

            try:
                ReportEndDate = datetime.strptime(ReportEndDate_str, '%B %d, %Y').date()
            except ValueError:
                ReportEndDate = None

            # Print the extracted dates
            print("Report Start Date:", ReportStartDate)
            print("Report End Date:", ReportEndDate)
        else:
            print("Invalid 'FROM' and 'TO' indices.")
    else:
        print("Could not find 'FROM' and 'TO' in the report period string.")
else:
    print("Report period string is null or empty.")
