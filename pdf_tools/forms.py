from django import forms  
class PdfForm(forms.Form):  
    file      = forms.FileField() # for creating file input  