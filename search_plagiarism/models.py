from django.db import models
import os
import json
from antiplagiarism.settings import MEDIA_URL, DEBUG
from .search_module import similar_image_finder as sif


if DEBUG:
    from dotenv import load_dotenv
    load_dotenv('env_keys.env')

database_url = os.environ['DATABASE_URL']
imgur_client_id = os.environ['IMGUR_CLIENT_ID']


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploaded/', null=True, blank=True)
    similar_images_list = models.CharField(max_length=1000, default='{}')
    probability_list = models.CharField(max_length=1000, default='{}')

    def __str__(self):
        return self.get_image_url()

    def get_images_probability_list(self):
        sif_obj = sif.SimilarImageFinder(database_url, imgur_client_id)
        path = MEDIA_URL + self.get_image_url()
        path = path[1:]
        images_probability_array = sif_obj.find_similar_images(path, 10)

        images_list = images_probability_array[0].tolist()
        probability_list = images_probability_array[1].tolist()

        for i in range(len(probability_list) - 1):
            probability_list[i] = (1 - probability_list[i]) * 100
        return [images_list, probability_list]

    def set_similar_images_list(self, images_list):
        imgur_images_list = []
        for i in range(len(images_list) - 1):
            imgur_images_list.append(images_list[i].replace('\n', ''))
        self.similar_images_list = json.dumps(imgur_images_list)
        self.save()

    def get_similar_images_list(self):
        return json.loads(self.similar_images_list)

    def set_probability_list(self, probability_list):
        self.images_probability_list = json.dumps(probability_list)
        self.save()

    def get_probability_list(self):
        return json.loads(self.probability_list)

    def start_finding(self):
        images_probability = self.get_images_probability_list()
        images = images_probability[0]
        probability = images_probability[1]
        self.set_similar_images_list(images)
        self.set_probability_list(probability)

    def get_image_url(self):
        return self.image.name


obj = UploadedImage()
