'''
import PyPDF2
import pandas as pd

# Path to the PDF file
pdf_path = r"D:\AIF Intern\Accounting\test\2021.pdf"

# Initialize an empty list to store extracted text
all_text = []

# Open the PDF file in read-binary mode
with open(pdf_path, "rb") as pdf_file:
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Iterate through each page of the PDF
    for i in range(2, len(pdf_reader.pages)):  # Start from page 2
        # Get the page object
        page = pdf_reader.pages[i]

        # Extract text from the current page
        page_text = page.extract_text()

        # Append the text to the list
        all_text.append(page_text)

# Combine all extracted text into a single string
combined_text = "\n".join(all_text)


# Process the combined text to separate rows and columns
rows = []
current_row = []

# Iterate through each line of text
for line in combined_text.split("\n"):
    # Split the line based on whitespace
    elements = line.split()

    # If the line is not empty
    if elements:
        # Add elements to the current row
        current_row.extend(elements)
    else:
        # If the line is empty, add the current row to the list of rows
        rows.append(current_row)
        # Reset the current row
        current_row = []

# If there are remaining elements in the current row, add it to the list of rows
if current_row:
    rows.append(current_row)

# Extract the column names from the first row
columns = rows[0]

# Create a DataFrame with the remaining rows and specified columns
df = pd.DataFrame(rows[1:], columns=columns)
print(df)


print(combined_text)
'''

''' remove headers 
import PyPDF2
import pandas as pd

# Path to the PDF file
pdf_path = r"D:\AIF Intern\Accounting\test\2021.pdf"

# Initialize an empty list to store extracted text
all_text = []
start_extraction = False
end_extraction = False
header_extracted = False
header = ""

# Open the PDF file in read-binary mode
with open(pdf_path, "rb") as pdf_file:
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Iterate through each page of the PDF
    for i in range(1, len(pdf_reader.pages)):  # Start from page 2
        # Get the page object
        page = pdf_reader.pages[i]

        # Extract text from the current page
        page_text = page.extract_text()

        # Skip extracting the header if already extracted
        if not header_extracted:
            header_lines = page_text.split("\n")
            header = "\n".join(header_lines[:8])  # Assuming the header is 8 lines
            header_extracted = True
            continue

        # Check if the specific string "TRANSFERFROMAFFILIATED" is in the page text
        if "TRANSFERFROMAFFILIATED" in page_text:
            # Set the flag to stop extraction
            end_extraction = True

        # Stop extraction if end flag is set
        if end_extraction:
            break

        # Append the text to the list
        all_text.append(page_text)

# Combine all extracted text into a single string
combined_text = "\n".join(all_text)

# Process the combined text to separate rows and columns
rows = []
current_row = []

# Iterate through each line of text
for line in combined_text.split("\n"):
    # Split the line based on whitespace
    elements = line.split()

    # If the line is not empty
    if elements:
        # Add elements to the current row
        current_row.extend(elements)
    else:
        # If the line is empty, add the current row to the list of rows
        rows.append(current_row)
        # Reset the current row
        current_row = []

# If there are remaining elements in the current row, add it to the list of rows
if current_row:
    rows.append(current_row)

# Extract the column names from the first row
columns = rows[0]

# Create a DataFrame with the remaining rows and specified columns
df = pd.DataFrame(rows[1:], columns=columns)
print(df)

'''

import pdfplumber

# Define the path to the PDF file
pdf_path = r"D:\AIF Intern\Accounting\test\2021.pdf"

def extract_and_modify_text(pdf_path):
    text = ''
    modified_rows = []
    # Flag to indicate if the extraction should continue
    continue_extraction = True

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages[2:]:
            # Adjusting x_tolerance for better handling of spaces
            text += page.extract_text(x_tolerance=1) + '\n'  # Adding a newline character for separation between pages

    lines = text.split("\n")

    # Iterate through the lines
    for idx, line in enumerate(lines):
        if idx == 0:
            line = line.replace("WEEKLY REPORT OF OPERATIONS ", "")
        elif idx == 1:
            parts = line.split("REPORT FOR THE PERIOD FROM ")[1].split("TO ")
            modified_rows.append(parts[0])
            modified_rows.append(parts[1])
            continue
        elif idx == 2:
            # Split the line into parts based on "Code :" and "Agency :"
            parts = line.split("Code : ")[1].split("Agency : ")
            modified_rows.append(parts[0])
            modified_rows.append(parts[1])
            continue
        elif idx == 3:
            # Split the line into parts based on "District :"
            parts = line.split("Name : ")[1].split("District : ")
            modified_rows.append(parts[0])
            modified_rows.append(parts[1])
            continue
        elif idx == 4:
            line = line.replace("Contract Date : ", "")
            # End the extraction after this line
        elif idx == 5:
            continue_extraction = False

        # Check if extraction should continue
        if continue_extraction:
            modified_rows.append(line)

    # Combine modified rows into a single string
    modified_text = "\n".join(modified_rows)

    return modified_text

# Extract and modify text from the PDF
modified_text = extract_and_modify_text(pdf_path)

# Print the modified text
print(modified_text)
