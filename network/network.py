from config import Config
import json
import http.client


class Network:

    def __init__(self, config: Config):
        self.config = config
        url = self.config.get('NETWORK', 'ServerUrl')
        port = self.config.getint('NETWORK', 'ServerPort')
        self._orders_route = '/pyquarium/index.php/orders'
        self._connection = http.client.HTTPConnection(url, port)
        self._headers = {"Content-type": "application/json", "Accept": "application/json"}
        self.start()

    def start(self):
        pass

    def get_orders(self):
        self._connection.request("GET", self._orders_route + '/last', None, self._headers)
        response = self._connection.getresponse()
        if response.getcode() != 200:
            print('Unable to get orders')
            return None
        return response.read()

    def mark_order_as_executed(self, order_id: int):
        self._connection.request("POST", "%s/execute/%d" % (self._orders_route, order_id), json.dumps({id: order_id}),
                                 self._headers)
        response = self._connection.getresponse()
        response.read()
        if response.getcode() != 200:
            print('unable to mark order as executed: ', response.read())
