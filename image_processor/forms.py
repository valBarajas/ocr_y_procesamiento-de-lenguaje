from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField(label='Sube una imagen:')


