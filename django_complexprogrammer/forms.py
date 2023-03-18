from django import forms

class InstagrammDownloaderForm(forms.ModelForm):
    class Meta:
        fields='__all__'