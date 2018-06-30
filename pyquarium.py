from light.light import Light
from network.orders_updater import OrdersUpdater
from sensors_data import SensorsData
from config import Config
import threading


class Pyquarium:
    def __init__(self):
        self._light_stop_event = threading.Event()
        self._order_stop_event = threading.Event()
        self.sensors_data = SensorsData()
        self.config = Config()
        self.light = None
        self.orders_updater = None
        self.start()

    def start(self):
        try:
            is_working = False
            while True:
                if is_working is False:
                    is_working = True
                    threading.Thread(target=self.start_light_thread).start()
                    threading.Thread(target=self.start_orders_thread).start()
        except KeyboardInterrupt:
            self._light_stop_event.set()
            self._order_stop_event.set()

    def start_light_thread(self):
        self.light = Light(self._light_stop_event, self.sensors_data, self.config)

    def start_orders_thread(self):
        self.orders_updater = OrdersUpdater(self._order_stop_event, self.config)


# Main program logic follows:
if __name__ == '__main__':
    Pyquarium()
