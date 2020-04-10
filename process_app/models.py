from django.db import models
import json
from .module import similar_image_finder as sif
from os import listdir
from os.path import isfile, join
from antiplagiat.settings import MEDIA_URL

database_url = 'db.sqlite3'
imgur_client_id = '620e8fb724910b6'


class UploadedImage(models.Model):
    imageURL = models.ImageField(upload_to='uploaded/', null=True, blank=True)
    similar_images_list = models.CharField(max_length=1000, default='{}')

    def __str__(self):
        return self.imageURL.name + ": " + self.similar_images_list

    def get_images_list(self):
        # sif_obj = sif.SimilarImageFinder(database_url, imgur_client_id)
        # images_list = sif_obj.find_similar_images(self.imageURL, 5)

        # Тестовая загрузка
        mypath = 'media\\' + 'result'
        images_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        return images_list

    def set_similar_images_list(self, images_list):
        self.similar_images_list = json.dumps(images_list)

    def get_similar_images_list(self):
        return json.loads(self.similar_images_list)

    def start_finding(self):
        self.set_similar_images_list(self.get_images_list())

    def get_imageurl(self):
        return self.imageURL.name


obj = UploadedImage()
obj.start_finding()
