from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from pdf_tools.forms import PdfForm
from pdf_tools.my_function import convert_pdf2docs, handle_uploaded_file
from projects.views import send_file_

def index(request):
    if request.method == 'POST':
        pdf = PdfForm(request.POST, request.FILES)
        if pdf.is_valid():
            handle_uploaded_file(request.FILES['file'])
            input_file=request.FILES['file'].name
            result = convert_pdf2docs(input_file)
            print(result['Output File'])
            # send_file_(result['Output File'])
            return FileResponse(open(result['Output File'], 'rb'), as_attachment=True)
            # return render(request, "pdf_tools/index.html",{'form':pdf})
    else:
        pdf = PdfForm()
        return render(request, "pdf_tools/index.html",{'form':pdf})
    # input_file = "pc.pdf"
    # output_file = "pcs.docx"
    # convert_pdf2docs(input_file, output_file)
    # return render(request, 'pdf_tools/index.html')