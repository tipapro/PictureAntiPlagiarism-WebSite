from django.db import models


class UploadedImage(models.Model):
    image = models.ImageField(null=True, blank=True)
