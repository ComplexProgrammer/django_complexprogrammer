from django.shortcuts import render
from django.http import FileResponse, HttpResponse, JsonResponse
from pdf_tools.forms import PdfForm
from pdf_tools.models import File
from pdf_tools.my_function import convert_pdf2excel, convert_pdf2docs, handle_uploaded_file
from projects.views import send_file_

def index(request):
    if request.method == 'POST':  
        type= request.POST['type']
        file = request.FILES['file'].read()
        fileName= request.POST['filename']
        end = request.POST['end']
        path = '' + fileName
        if file=="" or fileName=="" or end=="":
            res = JsonResponse({'data':'Invalid Request'})
            return res
        else:
            with open(path, 'wb+') as destination: 
                destination.write(file)
            FileFolder = File()
            FileFolder.existingPath = fileName
            FileFolder.eof = end
            FileFolder.name = fileName
            FileFolder.save()
            if type=='pdf2docx':
                result = convert_pdf2docs(path)
                print(result['Output File'])
                res = JsonResponse({'data':'Uploaded Successfully','existingPath': fileName, 'result': result['Output File']})
                return res
            if type == 'pdf2excel':
                result=convert_pdf2excel(path)
                print(result)
                res = JsonResponse({'data':'Uploaded Successfully','existingPath': fileName, 'result': result})
                return res
            # if type == 'pdf2image':
            #     result = convert_pdf2image(path)
            #     print(result)
            #     res = JsonResponse({'data':'Uploaded Successfully','existingPath': fileName, 'result': result})
            #     return res


    else:
        return render(request, "pdf_tools/index.html")
    # input_file = "pc.pdf"
    # output_file = "pcs.docx"
    # convert_pdf2docs(input_file, output_file)
    # return render(request, 'pdf_tools/index.html')