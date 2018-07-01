from config import Config
from sensors_data import SensorsData
import json
import http.client


class Network:

    def __init__(self, config: Config):
        self.config = config
        url = self.config.get('NETWORK', 'ServerUrl')
        port = self.config.getint('NETWORK', 'ServerPort')
        self._orders_route = '/pyquarium/index.php/orders'
        self._sensors_data_route = '/pyquarium/index.php/sensors'
        self._connection = http.client.HTTPConnection(url, port)
        self._headers = {"Content-type": "application/json", "Accept": "application/json"}

    def post_sensors_data(self, sensors_data: SensorsData):
        serialized = json.dumps(sensors_data.__dict__)
        self._connection.request("POST", self._sensors_data_route, serialized, self._headers)
        response = self._connection.getresponse()
        response_body = response.read()
        if response.getcode() != 200:
            print('unable to post sensors data', response_body)

    def get_orders(self):
        self._connection.request("GET", self._orders_route + '/last', None, self._headers)
        response = self._connection.getresponse()
        response_body = response.read()
        if response.getcode() != 200:
            print('Unable to get orders', response_body)
            return None
        return response_body

    def mark_order_as_executed(self, order_id: int):
        self._connection.request("POST", "%s/execute/%d" % (self._orders_route, order_id), json.dumps({'id': order_id}),
                                 self._headers)
        response = self._connection.getresponse()
        response.read()
        if response.getcode() != 200:
            print('unable to mark order as executed')
