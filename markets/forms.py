from django import forms
from .models import Product, ProductImage

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['store', 'name', 'category', 'price']

class ProductImageForm(forms.ModelForm):
    image = forms.FileField(
        widget=forms.FileInput(attrs={'allow_multiple_selected': True}),
        label='Images',
        required=False
    )

    class Meta:
        model = ProductImage
        fields = ['product', 'type', 'image']