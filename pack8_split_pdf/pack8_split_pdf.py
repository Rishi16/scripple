import PyPDF2
import re
import os
from pdfminer import high_level

input_path = "Invoices/Month"
for file in os.listdir(input_path):
    pdf_file = input_path + '/' + file
    print("Processing File: " + file)
    pdfReader = PyPDF2.PdfFileReader(open(pdf_file, 'rb'))
    no_of_pages = pdfReader.numPages
    print("Pages: " + str(no_of_pages))
    invoices = {}
    invoice_no = None
    for page in range(no_of_pages):
        print("Analyzing page: " + str(page))
        pageObj = pdfReader.getPage(page)
        text = high_level.extract_text(pdf_file, "", [page])
        cur_invoice_no = re.findall('Invoice#INV-\d+', text)
        date = re.findall('CINPAN\d+/\d+/\d+', text)
        if not date:
            date = re.findall('Invoice Date: \d+/\d+/\d+', text)
        if cur_invoice_no:
            invoice_no = cur_invoice_no[0].replace("Invoice#", "")
            invoices[invoice_no] = {}
            invoices[invoice_no]["pages"] = [page]
            if date:
                date = date[0].replace('CINPAN', '').replace('/', '-').replace('Invoice Date: ', '')
                invoices[invoice_no]["date"] = date
        else:
            invoices[invoice_no]["pages"].append(page)
    print("Analyzed: " + str(invoices))
    for invoice_no, details in invoices.items():
        print("Writing: " + str(invoice_no) + "\t" + str(details))
        output = PyPDF2.PdfFileWriter()
        for i in details["pages"]:
            output.addPage(pdfReader.getPage(i))
        with open("Invoices/with_dates/" + invoice_no + "_" + details["date"] + ".pdf", "wb") as outputStream:
            output.write(outputStream)
        with open("Invoices/without_dates/" + invoice_no + ".pdf", "wb") as outputStream:
            output.write(outputStream)
