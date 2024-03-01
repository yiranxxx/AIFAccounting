import datetime
import re



def split_transfer_data(text):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if "TRANSFER FROM AFFILIATED" in line and i + 1 < len(lines):
            data_row = lines[i + 1]
            # Regular expression to capture the structured data into seven groups
            match = re.match(r"\((\d+)\) ([A-Z ]+) (\d+-[A-Za-z]+-\d+) (Transfer XFR) (\d+\.\d+) \((\$\d+\.\d+)\) \((\$\d+\.\d+)\)", data_row)
            if match:
                ReportID = "IA_20210626_20210702_XIFENG"
                BankNumber = match.group(1)
                InsuredName = match.group(2)
                TransactionDate = match.group(3)
                TransactionType = match.group(4)
                CommissionPer = match.group(5)
                AmountDue = match.group(6)
                Balance = match.group(7)
                TimeStamp = datetime.datetime.now()
                return   ReportID, BankNumber, InsuredName, TransactionDate, TransactionType, CommissionPer, AmountDue, Balance, TimeStamp
    return None


