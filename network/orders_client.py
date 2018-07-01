from config import Config
from network.threaded_client import ThreadedClient
import json


class OrdersClient(ThreadedClient):

    def __init__(self, stop_event, config: Config):
        ThreadedClient.__init__(self, stop_event, config)

    def update(self):
        orders = self._network.get_orders()
        if orders is not None:
            new_orders = json.loads(orders)
            if type(new_orders) is dict:
                self.update_config(new_orders)
        super(OrdersClient, self).update()

    def update_config(self, data: dict):
        if data.get('sunriseTime') is not None:
            self.config.set('SUNCYCLE', 'Sunrise', data.get('sunriseTime'))
        if data.get('sunsetTime') is not None:
            self.config.set('SUNCYCLE', 'Sunset', data.get('sunsetTime'))
        self.config.write()
        self._network.mark_order_as_executed(data.get('id'))
