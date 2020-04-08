from django import forms
from process_app.models import UploadedImage


class UploadedImageForm(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = UploadedImage
        fields = ('image',)
