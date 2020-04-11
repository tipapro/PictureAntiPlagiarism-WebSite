from keras.applications import inception_v3
from keras.engine import Model
from keras.preprocessing.image import img_to_array
from PIL import Image
from numpy import zeros

class VectorizationModel:
    def prepare_image(self, image_path):
        img = Image.open(image_path)
        img.resize((299, 299), resample=Image.BILINEAR)
        return img_to_array(img)   # convert to keras format

    def prepare_vectorization_model(self, weights_path):
        self.__model__ = inception_v3.InceptionV3(include_top=True, weights=weights_path, classes=7)
        self.__model__ = Model(self.__model__.input, self.__model__.get_layer(index=-3).output)

    def vectorize(self, image_path):
        X = zeros((1, 299, 299, 3))
        X[0] = self.prepare_image(image_path) / 255
        image_vec = self.__model__.predict(X).reshape((1, -1))[0]
        return image_vec

    def vectorize_any(self, image_paths, weights_path):
        X = zeros((len(image_paths), 299, 299, 3))
        for i in range(len(image_paths)):
            X[i] = self.prepare_image(image_paths[i]) / 255
        image_vecs = self.__model__.predict(X).reshape((len(image_paths), -1))
        return image_vecs
