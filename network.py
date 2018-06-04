from config import Config
from sensors_data import SensorsData
import json


class Network():

    def __init__(self):
        self.config = Config()
        self.url = self.config.get('NETWORK', 'ServerUrl')

    def post_data(self, sensors_data: SensorsData):
        json_data = json.dumps(sensors_data.__dict__)
