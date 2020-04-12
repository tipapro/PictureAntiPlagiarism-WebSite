from .data_provider import ImageDataProvider


class ImageIterator:
    __chunk_size__ = 100

    def __init__(self, database_url):
        self.__data_provider__ = ImageDataProvider(database_url)
        self.__data_provider__.connect()
        self.count = self.__data_provider__.count()

    def __iter__(self):
        print(f'Reset iterator')
        self.__cur_pos__ = 0
        self.__cur_arr_pos__ = 0
        self.__cur_arr_id__, self.__cur_arr_vec__ = self.__data_provider__.get(0, self.__chunk_size__)
        return self

    def __next__(self):
        print(f'Current pos {self.__cur_pos__}')
        if self.__cur_pos__ < self.count:
            if self.__cur_arr_pos__ < self.__chunk_size__:
                image_ids, arr = self.__cur_arr_id__[self.__cur_arr_pos__], self.__cur_arr_vec__[self.__cur_arr_pos__]
                self.__cur_arr_pos__ += 1
                self.__cur_pos__ += 1
                return image_ids, arr
            else:
                self.__download_next_arrs__(self.__cur_pos__)
                self.__cur_arr_id__, self.__cur_arr_vec__ = self.__next_arr_id__, self.__next_arr_vec__
                self.__cur_arr_pos__ = 0
                image_ids, arr = self.__cur_arr_id__[self.__cur_arr_pos__], self.__cur_arr_vec__[self.__cur_arr_pos__]
                self.__cur_arr_pos__ += 1
                self.__cur_pos__ += 1
                return image_ids, arr
        else:
            raise StopIteration

    def __download_next_arrs__(self, start):
        print(f'Preloading from {start} to {start + self.__chunk_size__}')
        self.__next_arr_id__, self.__next_arr_vec__ = self.__data_provider__.get(start, self.__chunk_size__)