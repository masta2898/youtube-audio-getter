class AudioFile:
    def __init__(self, name, data):
        self.__name = name
        self.__data = data

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_data(self, data):
        self.__data = data

    def get_data(self):
        return self.__data
