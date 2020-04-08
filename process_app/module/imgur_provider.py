from PIL import Image
import requests


class ImgurClient:
    __get_image_url__ = 'https://api.imgur.com/3/image/'
    __upload_image_url__ = 'https://api.imgur.com/3/upload'

    def __init__(self, client_id):
        self.client_id = client_id

    def upload_image(self, path):
        """
        :param client_id: client id of your imgur.com application\n
        :param path: path of image file you want to upload\n
        :returns: id of uploaded image
        """
        img = Image.open(path)
        if img.format not in ['JPEG', 'PNG', 'GIF', 'APNG', 'TIFF']:
            path = path + '.png'
            img.save(path)
        file = open(path, 'rb')
        response = requests.post(self.__upload_image_url__, files={'image': file}, headers={'Authorization': 'Client-ID ' + self.client_id})
        file.close()
        response.raise_for_status()
        return response.json()['data']['id']

    def download_image(self, image_id):
        """
        :param client_id: client id of your imgur.com application\n
        :param image_id: id of image you want to download\n
        :returns: path of image file
        """
        file = open('new_file', 'wb')
        response = requests.get(self.__get_image_url__ + image_id, headers={'Authorization' : 'Client-ID ' + self.client_id})
        response.raise_for_status()
        link = response.json()['data']['link']
        response = requests.get(link)
        response.raise_for_status()
        file.write(response.content)
        file.close()
        return file.name
