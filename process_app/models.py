from django.db import models


class UploadedImage(models.Model):
    imageURL = models.ImageField(null=True, blank=True)
