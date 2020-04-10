from django import forms
from search_plagiarism.models import UploadedImage


class UploadedImageForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ('image',)