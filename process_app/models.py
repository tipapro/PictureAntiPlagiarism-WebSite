from django.db import models


class UploadImage(models.Model):
    image = models.ImageField(upload_to='image_temp', null=True, blank=True)

