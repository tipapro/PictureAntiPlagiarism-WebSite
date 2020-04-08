from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError

from process_app.models import UploadedImage
from process_app.forms import UploadedImageForm
from .similar_pictures_finder import SimilarPicturesFinder

import os
database_url = os.environ['DATABASE_URL']
imgur_client_id = os.environ['IMGUR_CLIENT_ID']


a = SimilarPicturesFinder
# список похожих картинок
similar_pictures_output = []


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
            processing()
        return render(request, 'process_app/process.html')
    else:
        form = UploadedImageForm()
    return render(request, 'process_app/index.html', {'form': form})


def processing():

    pass
