# used to get details about this pdf
# edit this, remove Print()s, return the info
# this assumes pdf file exists so add try catch
import PyPDF2


def get_Metadata(pdf_file):                     # pass in the pdf file
    with open(pdf_file, 'rb') as pdf_file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        info = pdf_reader.metadata              # info contains ALL details: can return
        print(info)                             # metadata in dictionary
        author = info.author                    # author name
        print(author)
        title = info.title                      # pdf title
        print(title)
        pages = len(pdf_reader.pages)           # number of pages
        print(pages)                            # can return any or all above


def extract_pg1_text(pdf_file):                     # pass in the pdf file
    with open(pdf_file, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        textpg1 = pdf_reader.pages[0].extract_text()  # text on page 1 to return
        print(textpg1)


pdf_file = 'Mags/42.pdf'                                # test pdf
get_Metadata(pdf_file)                                  # call
#extract_pg1_text(pdf_file)                              # call
