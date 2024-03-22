import pandas as pd
import glob
import os

from Extract_PDF_Function import Extract_PDF
from Clean_Info_Function import Clean_Info
from Clean_Detail_Function import Clean_Detail
from Clean_Payment_Function import Clean_Payment
from Public.Detect_PDF_Files_Function import Detect_PDF
from Public.Manipulate_PDF_Files_Function import Move_PDF, Copy_PDF
from dbutilities.Database_Function import Insert_DB, Check_Commission_Id_Exists
from Public.Write_Log_Function import Write_Log


directory_path = r"D:\AIF(Lisa)\Projects\Accounting ETL from pdf\test\IA original"
Institution_Name = "iA"
pdf_files = Detect_PDF(directory_path, Institution_Name)
print(type(pdf_files))