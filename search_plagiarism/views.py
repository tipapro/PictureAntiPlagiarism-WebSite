from django.shortcuts import render

from .models import *
from search_plagiarism.forms import UploadedImageForm, SimilarImagesForm


def index_upload_image(request):
    print('upload')
    if request.method == 'POST':
        form = UploadedImageForm(request.POST, request.FILES, )
        if form.is_valid():
            img = form.cleaned_data.get('image')
            obj.image = img
            obj.save()
            print(obj)
        return render(request, 'search_plagiarism/process.html')
    else:
        form = UploadedImageForm()
    return render(request, 'search_plagiarism/index.html', {'form': form})


def display_similar_images(request):
    if request.method == 'GET':
        return render(request, 'search_plagiarism/result.html')
    else:
        obj.start_finding()
    return render(request, 'search_plagiarism/result.html',
                  {'uploaded_image': obj.image, 'similar_images': obj.get_similar_images_list()})
