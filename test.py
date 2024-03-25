from Clean_PaymentData_Function import Clean_Payment
from Extract_PDF_Function import Extract_PDF
from dbutilities.Database_Function import Insert_DB

# Define the file path
file_name = r"\\AIF-NAS01\AIF_Interns\202312\Accounting\ErrorFile\0325\Error cleaning data could not convert string to float 108.89n108.89 lisa\W9_Feb 25 - Mar 3, 2023.pdf"

# Unpack the returned tuple into df0, df1, and df2
df0, df1, df2 = Extract_PDF(file_name)
# Info_df, CommissionID, End_Date_Year, AdvisorName, WeekNumber, StartDate, EndDate = Clean_Info(df0, "iA")
CommissionID = "iA_2021-09-03_212946(000)"
PaymentData_df = Clean_Payment(df1, df2, CommissionID)
# Detail_df = Clean_Detail(df1, df2, CommissionID)


Insert_DB(PaymentData_df)
print("Success")
