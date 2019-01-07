class AudioFile:
    def __init__(self, name, data):
        self.__name = name
        self.__filename = data

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_filename(self, filename):
        self.__filename = filename

    def get_filename(self):
        return self.__filename
