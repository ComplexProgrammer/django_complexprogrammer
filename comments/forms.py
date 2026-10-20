from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Comment
        fields = ["username", "email", "text", "page_url"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "page_url": forms.HiddenInput(),
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def clean_text(self):
        text = self.cleaned_data["text"].strip()
        if len(text) > 3000:
            raise forms.ValidationError("Izoh 3000 belgidan oshmasin")
        # "55555", "...", "Ok" kabi ma'nosiz izohlar (bazadagi izohlarning ~22% shunday edi)
        if len(text) < 5 or not any(ch.isalpha() for ch in text):
            raise forms.ValidationError("Izoh juda qisqa: fikringizni to'liqroq yozing")
        return text
