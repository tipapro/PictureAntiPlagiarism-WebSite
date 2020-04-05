from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from process_app.models import UploadImage
from process_app.forms import UploadImageForm


def result(request):
    return render(request, 'result.html')


def upload_image(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            uploaded_image = request.FILES['img']
            fs = FileSystemStorage()
            name = fs.save(uploaded_image.name, uploaded_image)
            url = fs.url(name)
    else:
        form = UploadImageForm()
    return render(request, 'index.html', {'form': form})
