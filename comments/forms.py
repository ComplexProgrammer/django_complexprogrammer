from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Comment
        fields = ['username', 'email', 'text', 'page_url']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'page_url': forms.HiddenInput(),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }