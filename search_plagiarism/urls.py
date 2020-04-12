from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from .views import *


urlpatterns = [
    path('', index_upload_image, name='upload_image'),
    path('', display_similar_images, name='display'),
    path('result/', display_similar_images, name='display'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
