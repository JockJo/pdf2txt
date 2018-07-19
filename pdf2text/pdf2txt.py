from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams,LTTextBoxHorizontal
from pdfminer.converter import PDFPageAggregator


# Open a PDF file.
fp = open(r'E:\document\patent\grant_pdf_20180102\P20180102-20180102\PP\028\837\PP028837.pdf', 'rb')
# Create a PDF parser object associated with the file object.
parser = PDFParser(fp)
# Create a PDF document object that stores the document structure.
# Supply the password for initialization.
document = PDFDocument(parser, '')
# Check if the document allows text extraction. If not, abort.
if not document.is_extractable:
    raise PDFTextExtractionNotAllowed
# Create a PDF resource manager object that stores shared resources.
rsrcmgr = PDFResourceManager()
# Create a PDF device object.
#device = PDFDevice(rsrcmgr)
# Set parameters for analysis.
laparams = LAParams()
# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
for page in PDFPage.create_pages(document):
    interpreter.process_page(page)
    # receive the LTPage object for the page.
    layout = device.get_result()
    for x in layout:
        if (isinstance(x, LTTextBoxHorizontal)):
            with open(r'1.txt', 'a',encoding='utf-8') as f:
                results = x.get_text()
                print(results)
                f.write(results + '\n')
# Create a PDF interpreter object.
#interpreter = PDFPageInterpreter(rsrcmgr, device)
# Process each page contained in the document.
#for page in PDFPage.create_pages(document):
#    interpreter.process_page(page)