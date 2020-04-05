from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from .views import *


urlpatterns = [
    path('result/', result, name='result'),
    path('', upload_image, name='upload_image')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
