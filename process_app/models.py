from django.db import models


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='MEDIA_ROOT', null=True, blank=True)

