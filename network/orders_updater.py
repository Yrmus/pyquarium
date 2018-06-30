from network.network import Network
from config import Config
import threading
import sched
import time
import json


class OrdersUpdater(threading.Thread):

    def __init__(self, stop_event, config: Config):
        threading.Thread.__init__(self)
        self.config = config
        self._stop_event = stop_event
        self._scheduler = sched.scheduler(time.time, time.sleep)
        self._network = Network(config)
        self._scheduler.enter(2, 1, self.update)
        self._scheduler.run()

    def update(self):
        new_orders = json.loads(self._network.get_orders())
        if new_orders is not None and type(new_orders) is dict:
            self.update_config(new_orders)
        if not self._stop_event.is_set():
            self._scheduler.enter(2, 1, self.update)

    def update_config(self, data: dict):
        if data.get('sunriseTime') is not None:
            self.config.set('SUNCYCLE', 'Sunrise', data.get('sunriseTime'))
        if data.get('sunsetTime') is not None:
            self.config.set('SUNCYCLE', 'Sunset', data.get('sunsetTime'))
        self.config.write()
        self._network.mark_order_as_executed(data.get('id'))
