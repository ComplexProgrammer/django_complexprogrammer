# from pdf2docx import parse
# # from pdf2image.pdf2image import convert_from_path
# import tabula
# # from webpage2pdf import RenderManager
# from typing import Tuple

# def convert_pdf2docs(input_file :str, pages: Tuple = None): # type: ignore
#     output_file=input_file[:-4] + ".docx"
#     if pages:
#         pages = [int(i) for i in list(pages) if i.isnumeric()] # type: ignore
#     result = parse(pdf_file=input_file,
#                    docx_file= output_file, pages=pages) # type: ignore

#     summary = {
#         "File" : input_file, "Pages": str(pages), "Output File": output_file
#     }

#     print("## Summary #########################################################")
#     print("\n".join("{}:{}".format(i, j) for i , j in summary.items()))
#     print("#####################################################################")
#     return summary

# def convert_pdf2excel(input_file):
#     # df = tabula.io.read_pdf(input_file, pages='all')
#     # print(df)
#     tabula.io.convert_into(input_file, input_file.replace(".pdf",".csv"), output_format="csv", pages='all')
#     return input_file.replace(".pdf",".csv")

# # def convert_pdf2image(input_file):
# #     pages = convert_from_path(input_file, 500, poppler_path=r'C:\poppler-23.11.0\Library\bin')
# #     i=0
# #     for page in pages:                    
# #         i=i+1
# #         page.save(i.__str__() +'-'+input_file.lower().replace(".pdf",".jpg"),'JPEG')
# #     return '1-'+input_file.lower().replace(".pdf",".jpg")

# # def url_to_pdf(url):
# #     rm=RenderManager()
# #     rm.addRender(num=2,showUI=True)
# #     rm.from_url(url,'0.pdf')
# #     rm.from_html("Hello World!",'1.pdf')
# #     #rm.from_localFile('html/test.html','2.pdf')
# #     print('start.')
# #     rm.waitFinish()
# #     print('finish all.')		
# #     return '0.pdf'

# def handle_uploaded_file(f):  
#     with open('static/upload/'+f.name, 'wb+') as destination:  
#         for chunk in f.chunks():  
#             destination.write(chunk)  