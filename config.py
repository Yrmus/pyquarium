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

    def set(self, section: str, option: str, value: str):
        self.config.set(section, option, value)

    def write(self):
        with open('config.ini', 'w') as config_file:
            self.config.write(config_file)
            config_file.close()
