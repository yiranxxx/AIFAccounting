import pdfplumber
import os
import csv

os.chdir(r"D:\AIF Intern\Accounting\test")

# Open PDF file
with pdfplumber.open("2022.pdf") as pdf:
    # Initialize an empty list to store all tables from page 3 and onwards
    all_tables = []

    # Iterate over pages starting from page 3
    for page in pdf.pages:
        # Check if the word "TRANSFERFROMAFFILIATED" is in the text
        #if "TRANSFER" in page.extract_text():
            #break  # Stop extraction if the word is found
        # Extract tables from the current page
        tables = page.extract_tables(table_settings={"vertical_strategy": "explicit", "horizontal_strategy": "text", "explicit_vertical_lines": [1,10]})
        # Extend the list of all tables with the tables from the current page
        all_tables.extend(tables)

# Write the extracted data to a CSV file
with open("extracted_data2.csv", mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for table in all_tables:
        for row in table:
            writer.writerow(row)



