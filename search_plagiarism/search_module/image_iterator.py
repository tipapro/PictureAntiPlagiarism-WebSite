from .data_provider import ImageDataProvider


class ImageIterator:
    __chunk_size__ = 100

    def __init__(self, database_url):
        self.__data_provider = ImageDataProvider(database_url)
        self.__data_provider.connect()
        self.count = self.__data_provider.count()

    def __iter__(self):
        print(f'Reset iterator')
        self.__cur_pos = 0
        self.__cur_arr_pos = 0
        self.__cur_arr_id, self.__cur_arr_vec = self.__data_provider.get(0, self.__chunk_size)
        return self

    def __next__(self):
        print(f'Current pos {self.__cur_pos__}')
        if self.__cur_pos < self.count:
            if self.__cur_arr_pos < self.__chunk_size:
                image_ids, arr = self.__cur_arr_id[self.__cur_arr_pos], self.__cur_arr_vec[self.__cur_arr_pos]
                self.__cur_arr_pos += 1
                self.__cur_pos += 1
                return image_ids, arr
            else:
                self.__download_next_arrs(self.__cur_pos)
                self.__cur_arr_id, self.__cur_arr_vec = self.__next_arr_id, self.__next_arr_vec
                self.__cur_arr_pos__ = 0
                image_ids, arr = self.__cur_arr_id[self.__cur_arr_pos], self.__cur_arr_vec[self.__cur_arr_pos]
                self.__cur_arr_pos += 1
                self.__cur_pos += 1
                return image_ids, arr
        else:
            raise StopIteration

    def __download_next_arrs__(self, start):
        print(f'Preloading from {start} to {start + self.__chunk_size__}')
        self.__next_arr_id, self.__next_arr_vec = self.__data_provider.get(start, self.__chunk_size)
