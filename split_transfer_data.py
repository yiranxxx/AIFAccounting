import datetime
import re

from Extract_wholetext_from_pdf import extract_wholetext_from_pdf


def split_transfer_data(text):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if "TRANSFER FROM AFFILIATED" in line and i + 1 < len(lines):
            data_row = lines[i + 1]
            # Regular expression to capture the structured data into seven groups
            match = re.match(
                r"\((\d+)\) ([A-Z ]+) (\d+-[A-Za-z]+-\d+) (Transfer XFR) (\d+\.\d+) \((\$\d+\.\d+)\) \((\$\d+\.\d+)\)",
                data_row)
            if match:
                ReportID = "IA_20210626_20210702_XIFENG_006"
                BankNumber = match.group(1)
                InsuredName = match.group(2)
                TransactionDate = match.group(3)
                TransactionType = match.group(4)
                CommissionPer = match.group(5)
                AmountDue = match.group(6)
                Balance = match.group(7)
                TimeStamp = datetime.datetime.now()
                return ReportID, BankNumber, InsuredName, TransactionDate, TransactionType, CommissionPer, AmountDue, Balance, TimeStamp
    return None


pdf_path = r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\Jun 26 - July 2, 2021 - Mock.pdf'
content = extract_wholetext_from_pdf(pdf_path)
params = split_transfer_data(content)  # Ensure this function returns data in the correct order and format

if params:
    print(
        f"BankNumber: {params[0]},BankNumber: {params[1]}, InsuredName: {params[2]}, TransactionDate: {params[3]}, TransactionType: {params[4]}, CommissionPer: {params[5]}, AmountDue: {params[6]}, Balance: {params[6],}, TimeStamp: {params[7],}")
else:
    print("Data not found or format is inconsistent.")
