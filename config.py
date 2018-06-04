import configparser


class Config:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    def getint(self, section: str, option: str):
        return self.config.getint(section, option)

    def getboolean(self, section: str, option: str):
        return self.config.getboolean(section, option)

    def get(self, section: str, option: str):
        return self.config.get(section, option)

