import pdfplumber

pdf_path = r'D:\AIF(Lisa)\Projects\Accounting ETL from pdf\Jun 26 - July 2, 2021 - Mock.pdf'

def extract_wholetext_from_pdf(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Adjusting x_tolerance for better handling of spaces
            text += page.extract_text(x_tolerance=1) + '\n'  # Adding a newline character for separation between pages
    return text

content = extract_wholetext_from_pdf(pdf_path)
print(content)
