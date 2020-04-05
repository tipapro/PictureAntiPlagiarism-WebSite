from django import forms
from process_app.models import UploadImage


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UploadImage
        fields = ('image',)
