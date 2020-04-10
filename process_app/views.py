from django.shortcuts import render

from .models import *
from process_app.forms import UploadedImageForm


def index_upload_image(request):
    print('upload')
    if request.method == 'POST':
        form = UploadedImageForm(request.POST, request.FILES,)
        if form.is_valid():
            img = form.cleaned_data.get('image')
            obj.imageURL = img
            obj.save()
            print(obj)
        return render(request, 'process_app/process.html')
    else:
        form = UploadedImageForm()
    return render(request, 'process_app/index.html', {'form': form})


def result(request):
    return render(request, 'process_app/result.html',
                  {'similar_images': obj.get_similar_images_list(), 'uploaded_image': obj.get_imageurl()})


def display_similar_images(request):
    if request.method == 'GET':
        pass
    return render(request, 'process_app/result.html', )
