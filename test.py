from Clean_Detail_Function import Clean_Detail
from Clean_Info_Function import Clean_Info
from Clean_Payment_Function import Clean_Payment
from Extract_PDF_Function import Extract_PDF
from dbutilities.Database_Function import Insert_DB

# Define the file path
file_name = r"\\AIF-NAS01\AIF_Interns\202312\Accounting\ErrorFile\0326\Error cleaning data could not convert string\W21_May 20 - May 26, 2023.pdf"

# Unpack the returned tuple into df0, df1, and df2
df0, df1, df2 = Extract_PDF(file_name)
Info_df, CommissionID, End_Date_Year, AdvisorName, WeekNumber, StartDate, EndDate = Clean_Info(df0, "iA")


Detail_df = Clean_Detail(df1, df2, CommissionID)
PaymentData_df = Clean_Payment(df1, df2, CommissionID)


Insert_DB(Info_df,Detail_df,PaymentData_df)

print("Success")
