import pdfplumber
import re
import datetime
import csv

def extract_text_from_specific_page(pdf_path, target_page_number):
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            if i == target_page_number:
                # Adjusting x_tolerance for better handling of spaces
                return page.extract_text(x_tolerance=1)

    # Return None if the target page is not found
    return None

def extract_transfer_data(text):
    # Define patterns to match the required information
    file_number_pattern = re.compile(r"WEEKLY REPORT OF OPERATIONS ([A-Z0-9]+)")
    date_pattern = re.compile(r"REPORT FOR THE PERIOD FROM (\w+ \d+, \d+) TO (\w+ \d+, \d+)")
    advisor_code_pattern = re.compile(r"Code : (\d+) \((\d+)\)")
    advisor_name_pattern = re.compile(r"Name : (\w+ \w+)")
    contract_info_pattern = re.compile(r"Contract Date : (.+?) \(([^)]+)\)")

    # Initialize variables to store matched data
    report_start_date = ""
    report_end_date = ""
    file_number = ""
    advisor_code = ""
    advisor_name = ""
    contract_date = ""
    contract_status = ""

    # Iterate through lines to extract relevant information
    for line in text.split('\n'):
        file_number_match = file_number_pattern.match(line)
        date_match = date_pattern.match(line)
        advisor_code_match = advisor_code_pattern.match(line)
        advisor_name_match = advisor_name_pattern.match(line)
        contract_info_match = contract_info_pattern.match(line)

        if file_number_match:
            file_number = file_number_match.group(1)
        elif date_match:
            report_start_date = date_match.group(1)
            report_end_date = date_match.group(2)
        elif advisor_code_match:
            advisor_code = advisor_code_match.group(1) + " (" + advisor_code_match.group(2) + ")"
        elif advisor_name_match:
            advisor_name = advisor_name_match.group(1)
        elif contract_info_match:
            contract_date = contract_info_match.group(1)
            contract_status = contract_info_match.group(2) if contract_info_match.group(2) else ""

    # Try parsing dates with multiple formats
    try:
        report_start_date = datetime.datetime.strptime(report_start_date, "%B %d, %Y").date()
        report_end_date = datetime.datetime.strptime(report_end_date, "%B %d, %Y").date()
    except ValueError:
        pass  # Handle date parsing errors

    # Return data even if not everything matches
    return {
        "ReportStartDate": report_start_date,
        "ReportEndDate": report_end_date,
        "FileNumber": file_number,
        "AdvisorCode": advisor_code,
        "AdvisorName": advisor_name,
        "ContractDate": contract_date,
        "ContractStatus": contract_status
    }

# Replace 'your_file.pdf' with the path to your PDF file
pdf_path = r'C:\Users\fanzi\Desktop\AI Financial\Python\Jun 26 - July 2, 2021.pdf'
# Specify the target page number (in this case, page 3)
target_page_number = 3

# Extract text from the specified page of the PDF
content = extract_text_from_specific_page(pdf_path, target_page_number)

# Print the extracted data
print("\nExtracted Data:")
result = extract_transfer_data(content)
print(result)

def extract_agency_district_contract_status(text):
    # Define patterns to match the required information
    agency_pattern = re.compile(r"Agency : (.+)")
    district_pattern = re.compile(r"District : (.+)")

    # Initialize variables to store matched data
    agency = ""
    district = ""

    # Iterate through lines to extract relevant information
    for line in text.split('\n'):
        agency_match = agency_pattern.search(line)
        district_match = district_pattern.search(line)

        if agency_match:
            agency = agency_match.group(1).strip()
        elif district_match:
            district = district_match.group(1).strip()

    # Return data even if not everything matches
    return {
        "Agency": agency,
        "District": district
    }

# Replace 'your_file.pdf' with the path to your PDF file
pdf_path = r'C:\Users\fanzi\Desktop\AI Financial\Python\Jun 26 - July 2, 2021.pdf'
# Specify the target page number (in this case, page 3)
target_page_number = 3

# Extract text from the specified page of the PDF
content = extract_text_from_specific_page(pdf_path, target_page_number)

# Print the extracted data
result = extract_agency_district_contract_status(content)
print(result)

# Specify the CSV output file path
csv_output_path = 'output_data.csv'

# Write the extracted data to a CSV file
with open(csv_output_path, 'w', newline='', encoding='utf-8') as csv_file:
    fieldnames = result.keys()
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Write the data
    writer.writerow(result)