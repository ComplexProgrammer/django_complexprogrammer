from pdf2docx import parse
from typing import Tuple

def convert_pdf2docs(input_file :str, pages: Tuple = None): # type: ignore
    output_file=input_file[:-4] + ".docx"
    if pages:
        pages = [int(i) for i in list(pages) if i.isnumeric()] # type: ignore
    result = parse(pdf_file=input_file,
                   docx_file= output_file, pages=pages) # type: ignore

    summary = {
        "File" : input_file, "Pages": str(pages), "Output File": output_file
    }

    print("## Summary #########################################################")
    print("\n".join("{}:{}".format(i, j) for i , j in summary.items()))
    print("#####################################################################")
    return summary

def handle_uploaded_file(f):  
    with open('static/upload/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)  