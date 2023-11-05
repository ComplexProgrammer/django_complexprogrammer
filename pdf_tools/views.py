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
        existingPath = request.POST['existingPath']
        end = request.POST['end']
        nextSlice = request.POST['nextSlice']
        
        if file=="" or fileName=="" or existingPath=="" or end=="" or nextSlice=="":
            res = JsonResponse({'data':'Invalid Request'})
            return res
        else:
            if existingPath == 'null':
                path = 'media/' + fileName
                with open(path, 'wb+') as destination: 
                    destination.write(file)
                FileFolder = File()
                FileFolder.existingPath = fileName
                FileFolder.eof = end
                FileFolder.name = fileName
                FileFolder.save()
                if int(end):
                    res = JsonResponse({'data':'Uploaded Successfully','existingPath': fileName})
                else:
                    res = JsonResponse({'existingPath': fileName})
                return res

            else:
                path = 'media/' + existingPath
                model_id = File.objects.get(existingPath=existingPath)
                if model_id.name == fileName:
                    if not model_id.eof:
                        with open(path, 'ab+') as destination: 
                            destination.write(file)
                        if int(end):
                            model_id.eof = int(end) # type: ignore
                            model_id.save()
                            res = JsonResponse({'data':'Uploaded Successfully','existingPath':model_id.existingPath})
                        else:
                            res = JsonResponse({'existingPath':model_id.existingPath})    
                        return res
                    else:
                        res = JsonResponse({'data':'EOF found. Invalid request'})
                        return res
                else:
                    res = JsonResponse({'data':'No such file exists in the existingPath'})
                    return res
    # if request.method == 'POST':
    #     pdf = PdfForm(request.POST, request.FILES)
    #     if pdf.is_valid():
    #         handle_uploaded_file(request.FILES['file'])
    #         input_file=request.FILES['file'].name
    #         result = convert_pdf2docs(input_file)
    #         print(result['Output File'])
    #         # send_file_(result['Output File'])
    #         return FileResponse(open(result['Output File'], 'rb'), as_attachment=True)
    #         # return render(request, "pdf_tools/index.html",{'form':pdf})
    else:
        pdf = PdfForm()
        return render(request, "pdf_tools/index.html",{'form':pdf})
    # input_file = "pc.pdf"
    # output_file = "pcs.docx"
    # convert_pdf2docs(input_file, output_file)
    # return render(request, 'pdf_tools/index.html')