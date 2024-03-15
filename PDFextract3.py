import pdfplumber
import camelot
import os
import pandas as pd
import cv2
import re
import datetime

def extract_text_from_specific_page(pdf_path, target_page_number):
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            if i == target_page_number:
                # Adjusting x_tolerance for better handling of spaces
                return page.extract_text(x_tolerance=1)

    # Return None if the target page is not found
    return None

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
print("\nExtracted Data:")
result = extract_agency_district_contract_status(content)
print(result)
