from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError

from process_app.models import UploadedImage
from process_app.forms import UploadedImageForm


def index(request):
    print('index')
    return render(request, 'process_app/index.html')


def result(request):
    print('result')
    return render(request, 'result.html')


def upload_image(request):
    print('upload')
    if request.method == 'POST':
        form = UploadedImageForm(request.POST, request.FILES,)
        if form.is_valid():
            img = form.cleaned_data.get("image")
            obj = UploadedImage.objects.create(
                image=img
            )
            obj.save()
            print(obj)
        return render(request, 'process_app/process.html')
    else:
        form = UploadedImageForm()
    return render(request, 'process_app/index.html', {'form': form})
