import os
import glob

def Detect_PDF(top_folder, Institution_Name):
    # Prepare to store the paths of all found PDF files
    pdf_files = []

    # Traverse the top_folder
    for root, dirs, files in os.walk(top_folder):
        # Look for 'iA' folders at the third level
        if os.path.basename(root) == Institution_Name and root.count(os.sep) == top_folder.count(os.sep) + 2:
            # Traverse the 'iA' folder
            for ins_root, ins_dirs, ins_files in os.walk(root):
                # Look for the additional layer of folders
                if ins_root.count(os.sep) == root.count(os.sep) + 1:
                    # Use glob to find all PDF files in this folder
                    extra_pdf_files = glob.glob(os.path.join(ins_root, '*.pdf'))
                    # Add the found PDF files to the list
                    pdf_files.extend(extra_pdf_files)

    return pdf_files



#test
# directory_path = r"D:\AIF Intern\Accounting\Commission\OriginalFile"
# Institution_Name = "iA"
# pdf_files= Detect_PDF(directory_path, Institution_Name)
# for file in pdf_files:
#     print(file)


