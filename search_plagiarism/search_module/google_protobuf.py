import base64
from io import BytesIO

import numpy as np

from .image_vector_pb2 import ImageVector


class ImageVectorConverter:

    def serialize(self, image_id, vector):
        """
        :param image_id:
        :param vector: numpy list\n
        :returns: base64 serialized string
        """
        image_vec = ImageVector(id=image_id, vec=vector.tobytes())
        byte_array = image_vec.SerializeToString()
        return base64.b64encode(byte_array).decode()

    def deserialize(self, ser_string):
        """
        :param ser_string: base64 serialized string\n
        :returns: tuple (image_id, vector) where vector is a list of floats
        """
        image_vec = ImageVector()
        image_vec.ParseFromString(base64.b64decode(ser_string))
        return image_vec.id, np.frombuffer(image_vec.vec, dtype='f')
