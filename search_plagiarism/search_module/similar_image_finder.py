from .vectorization_model import VectorizationModel
from .image_iterator import ImageIterator
from scipy.spatial import distance
from .data_provider import ImageDataProvider
import numpy as np
from .imgur_provider import ImgurClient
from antiplagiarism.settings import STATIC_URL

path_to_model = 'antiplagiarism' + STATIC_URL + 'vectorization_model.h5'


class SimilarImageFinder:
    def __init__(self, database_url, imgur_client_id):
        self.__imgur_client_id__ = imgur_client_id
        self.__database_url__ = database_url
        self.__model__ = VectorizationModel()
        self.__model__.prepare_vectorization_model(path_to_model)
        self.__iterator__ = ImageIterator(database_url)

    def find_similar_images(self, image_path, count_of_similar_image, progress_notification=None):
        '''
        :returns: (image_ids, probability), 0 <= probability <= 1
        '''
        vec = self.__model__.vectorize(image_path)
        image_ids, probability = self.find_closest_vectors(vec, self.__iterator__, count_of_similar_image)
        probability = probability / 2
        return image_ids, probability

    def vectorize_and_send(self, image_path):
        vec = self.__model__.vectorize(image_path)
        db = ImageDataProvider(self.__database_url__)
        imgur_client = ImgurClient(self.__imgur_client_id__)
        image_id = imgur_client.upload_image(image_path)
        db.append(image_id, vec)


    def find_closest_vectors(self, target_image_vec, other_images_vecs, n_similar_imgs):
        '''
        :returns: (image_ids, cosine_distances), 0 <= cosine_distances <= 2
        '''
        other_images_vecs.__iter__()
        arr = np.ndarray(n_similar_imgs)
        image_ids = np.ndarray(n_similar_imgs, dtype=np.int)
        try:
            for i in range(0, n_similar_imgs):
                image_ids[i], vec = other_images_vecs.__next__()
                arr[i] = distance.cosine(target_image_vec, vec)
            sort_indices = np.argsort(arr)
            arr = arr[sort_indices]
            image_ids = image_ids[sort_indices]
            while True:
                image_id, vec = other_images_vecs.__next__()
                sim = distance.cosine(target_image_vec, vec)
                index = np.searchsorted(arr, sim)
                if index < n_similar_imgs:
                    i = n_similar_imgs - 1
                    while i != index:
                        arr[i] = arr[i - 1]
                        image_ids[i] = image_ids[i - 1]
                        i -= 1
                    image_ids[index], arr[index] = image_id, sim
        except StopIteration:
            pass
        return image_ids, arr
