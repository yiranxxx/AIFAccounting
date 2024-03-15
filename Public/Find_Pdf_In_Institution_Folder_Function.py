import glob
import os


def find_pdf_in_institution_folder(top_folder, InstitutionName):
    # Prepare to store the paths of all found PDF files
    pdf_files = []

    # Traverse the top_folder
    for root, dirs, files in os.walk(top_folder):
        # Look for 'IA' folders at the third level
        if os.path.basename(root) == InstitutionName and root.count(os.sep) == top_folder.count(os.sep) + 2:
            # Use glob to find all PDF files in this institution folder
            ia_pdf_files = glob.glob(os.path.join(root, '*.pdf'))
            # Add the found PDF files to the list
            pdf_files.extend(ia_pdf_files)

    return pdf_files

