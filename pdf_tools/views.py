from django.shortcuts import render
from django.http import HttpResponse
from pdf_tools.forms import PdfForm
from pdf_tools.my_function import convert_pdf2docs, handle_uploaded_file

def index(request):
    if request.method == 'POST':
        pdf = PdfForm(request.POST, request.FILES)
        if pdf.is_valid():
            handle_uploaded_file(request.FILES['file'])
            input_file=request.FILES['file'].name
            convert_pdf2docs(input_file)
            return render(request, "pdf_tools/index.html",{'form':pdf})
    else:
        pdf = PdfForm()
        return render(request, "pdf_tools/index.html",{'form':pdf})
    # input_file = "pc.pdf"
    # output_file = "pcs.docx"
    # convert_pdf2docs(input_file, output_file)
    # return render(request, 'pdf_tools/index.html')