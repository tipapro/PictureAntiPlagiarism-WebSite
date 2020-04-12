from django.db import models
import array
import json, os
import numpy as np
import codecs, json
from antiplagiarism.settings import MEDIA_URL, DEBUG
from .search_module import similar_image_finder as sif
from .search_module import imgur_provider as imgur

# Тест
from os import listdir
from os.path import isfile, join

if DEBUG:
    from dotenv import load_dotenv
    load_dotenv('env_keys.env')

database_url = os.environ['DATABASE_URL']
imgur_client_id = os.environ['CLIENT_ID']


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploaded/', null=True, blank=True)
    similar_images_list = models.CharField(max_length=1000, default='{}')
    images_probability_list = models.CharField(max_length=1000, default='{}')

    def __str__(self):
        return self.get_image_url() + ": " + str(self.get_similar_images_list())

    def get_images_probability_list(self):
        sif_obj = sif.SimilarImageFinder(database_url, imgur_client_id)
        images_probability_array = sif_obj.find_similar_images(r'search_plagiarism/search_module/pic1.jpg', 10)
        images_list = images_probability_array[0].tolist()
        probability_list = images_probability_array[1].tolist()

        for i in range(len(probability_list) - 1):
            probability_list[i] = (1 - probability_list[i]) * 100
        return [images_list, probability_list]

    def set_similar_images_list(self, images_list):
        imgur_images_list = []
        imgur_obj = imgur.ImgurClient(imgur_client_id)
        for i in range(len(images_list) - 1):
            imgur_images_list.append(imgur_obj.download_image(str(images_list[i])))
        self.similar_images_list = json.dumps(imgur_images_list)

    def get_similar_images_list(self):
        return json.loads(self.similar_images_list)

    def set_images_probability_list(self, probability_list):
        self.images_probability_list = json.dumps(probability_list)

    def get_images_probability_list(self):
        return json.loads(self.images_probability_list)

    def start_finding(self):
        images_probability = self.get_images_probability_list()
        images = images_probability[0]
        print(images)
        probability = images_probability[1]
        print(probability)
        self.set_similar_images_list(images)
        self.set_images_probability_list(probability)

    def get_image_url(self):
        return self.image.name


obj = UploadedImage()
