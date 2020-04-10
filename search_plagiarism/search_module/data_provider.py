from .postgresql import PostgreSQLClient
from .google_protobuf import ImageVectorConverter
import numpy as np
import time


class ImageDataProvider:
    __max_sleep_time__ = 64

    def __init__(self, database_url):
        self.__client__ = PostgreSQLClient(database_url)
        self.__converter__ = ImageVectorConverter()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def append(self, image_id, vector):
        data = self.__converter__.serialize(image_id, vector)
        i = 1
        while True:
            try:
                self.__client__.append([data])
                break
            except Exception as ex:
                if i >= self.__max_sleep_time__:
                    raise ex
                time.sleep(i)
                i *= 2
                continue

    def get(self, start, count):
        """
        :params: start min value is 1
        """
        i = 1
        data = ''
        while True:
            try:
                data = self.__client__.get_range(start, count)
                break
            except Exception as ex:
                if i >= self.__max_sleep_time__:
                    raise ex
                time.sleep(i)
                i *= 2
                continue
        data_length = len(data)
        arr_id, arr_vec = np.empty(data_length, object), np.empty(data_length, np.ndarray)
        for row, i in zip(data, range(0, data_length)):
            arr_id[i], arr_vec[i] = self.__converter__.deserialize(row[0])
        return arr_id, arr_vec

    def clear_all(self):
        i = 1
        while True:
            try:
                self.__client__.clear_all()
                break
            except Exception as ex:
                if i >= self.__max_sleep_time__:
                    raise ex
                time.sleep(i)
                i *= 2
                continue

    def count(self):
        i = 1
        while True:
            try:
                return self.__client__.get_count()
            except Exception as ex:
                if i >= self.__max_sleep_time__:
                    raise ex
                time.sleep(i)
                i *= 2
                continue

    def connect(self):
        self.__client__.connect()

    def close(self):
        self.__client__.close()
