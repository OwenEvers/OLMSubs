# used to get details about this pdf
# edit this, remove Print()s, return the info
# this assumes pdf file exists so add try catch
import PyPDF2


def get_Metadata(pdf_file):                     # pass in the pdf file

    direct = "Mags/"
    num = str(pdf_file)
    ext = ".pdf"
    pdf = f"{direct}{num}{ext}"
    try:
        with open(pdf, 'rb') as pdf_file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            info = pdf_reader.metadata  # info contains ALL details: can return metadata in dictionary
            #print(info)
            author = info.author  # author name
            title = info.title  # pdf title
            pages = len(pdf_reader.pages)  # number of pages

    except FileNotFoundError:
        pdf = 'error.pdf'
        with open(pdf, 'rb') as pdf_file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            info = pdf_reader.metadata  # info contains ALL details: can return metadata in dictionary
            #print(info)
            author = info.author  # author name
            title = info.title  # pdf title
            pages = len(pdf_reader.pages)  # number of pages

    #print(info)
    return info

def extract_pg1_text(pdf_file):                     # pass in the pdf file
    direct = "Mags/"
    num = str(pdf_file)
    ext = ".pdf"
    pdf = f"{direct}{num}{ext}"
    try:
        with open(pdf, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            textpg1 = pdf_reader.pages[0].extract_text()  # text on page 1 to return
            #print(textpg1)
    except FileNotFoundError:
        pdf = 'error.pdf'
        with open(pdf, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            textpg1 = pdf_reader.pages[0].extract_text()  # text on page 1 has error to return
    return textpg1

#pdf_file = '53'                                # test Number only .pdf
#get_Metadata(pdf_file)                                  # call
#extract_pg1_text(pdf_file)                              # call
