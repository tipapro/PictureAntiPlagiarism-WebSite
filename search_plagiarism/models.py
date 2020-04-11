from django.db import models
import sqlite3
import json, os
from antiplagiarism.settings import MEDIA_URL, DEBUG
from .search_module import similar_image_finder as sif

# Тест
from os import listdir
from os.path import isfile, join

if DEBUG:
    from dotenv import load_dotenv

    load_dotenv('env_keys.env')

database_url = os.environ['DATABASE_URL']  # '../db.sqlite3='
imgur_client_id = os.environ['CLIENT_ID']  # '620e8fb724910b6'


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploaded/', null=True, blank=True)
    similar_images_list = models.CharField(max_length=1000, default='{}')

    def __str__(self):
        return self.get_image_url() + ": " + str(self.get_similar_images_list())

    def get_images_list(self):
        sif_obj = sif.SimilarImageFinder(database_url, imgur_client_id)
        images_list = sif_obj.find_similar_images(r'search_plagiarism/search_module/pic1.jpg', 10)
        # # Тестовая загрузка
        # mypath = 'media\\' + 'result'
        # images_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        return images_list

    def set_similar_images_list(self, images_list):
        self.similar_images_list = json.dumps(images_list)

    def get_similar_images_list(self):
        return json.loads(self.similar_images_list)

    def start_finding(self):
        self.set_similar_images_list(self.get_images_list())

    def get_image_url(self):
        return self.image.name


obj = UploadedImage()
