from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from django.views.generic import RedirectView

from .views import *


urlpatterns = [
    path('', index_upload_image, name='index'),
    path('result/', result, name='result'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
