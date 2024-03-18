import os
import shutil

def Move_PDF(file, AdvisorName, Institution_Name, EndDate_Year):
    # Construct the destination folder path based on the provided parameters
    destination_folder = rf'D:\AIF Intern\Accounting\Commission\HistoryFile\{AdvisorName}\{Institution_Name}\{EndDate_Year}'

    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Move each PDF file to the destination folder
    file_name = os.path.basename(file)
    destination_path = os.path.join(destination_folder, file_name)
    shutil.move(file, destination_path)
    print(f"Moved {file_name} to {destination_folder}")


# test
# file = r'D:\AIF Intern\Accounting\Commission\OriginalFile\wang\iA\2024\W4_Jan 20 - Jan 26, 2024.pdf'
# AdvisorName = 'Wang'
# InstitutionName = 'iA'
# EndDate_Year = '2024'
# Move_PDF(file, AdvisorName, InstitutionName, EndDate_Year)
