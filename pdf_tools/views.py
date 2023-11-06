from django.shortcuts import render
from django.http import FileResponse, HttpResponse, JsonResponse
from pdf_tools.forms import PdfForm
from pdf_tools.models import File
from pdf_tools.my_function import convert_pdf2docs, handle_uploaded_file
from projects.views import send_file_

def index(request):
    if request.method == 'POST':  
        file = request.FILES['file'].read()
        fileName= request.POST['filename']
        end = request.POST['end']
        nextSlice = request.POST['nextSlice']
        
        if file=="" or fileName=="" or end=="" or nextSlice=="":
            res = JsonResponse({'data':'Invalid Request'})
            return res
        else:
            path = '' + fileName
            with open(path, 'wb+') as destination: 
                destination.write(file)
            FileFolder = File()
            FileFolder.existingPath = fileName
            FileFolder.eof = end
            FileFolder.name = fileName
            FileFolder.save()
            result = convert_pdf2docs(path)
            print(result['Output File'])
            res = JsonResponse({'data':'Uploaded Successfully','existingPath': fileName, 'result': result['Output File']})
            return res
    else:
        return render(request, "pdf_tools/index.html")
    # input_file = "pc.pdf"
    # output_file = "pcs.docx"
    # convert_pdf2docs(input_file, output_file)
    # return render(request, 'pdf_tools/index.html')