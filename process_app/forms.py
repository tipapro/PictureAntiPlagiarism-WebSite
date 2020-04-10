from django import forms
from process_app.models import UploadedImage


class UploadedImageForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ('imageURL',)
