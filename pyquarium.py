from light.light import Light
from network.orders_client import OrdersClient
from network.sensors_client import SensorsClient
from sensors_data import SensorsData
from config import Config
import threading


class Pyquarium:
    def __init__(self):
        self._stop_event = threading.Event()
        self.sensors_data = SensorsData()
        self.config = Config()
        self.light = None
        self.orders_client = None
        self.sensors_client = None
        self.start()

    def start(self):
        try:
            is_working = False
            while True:
                if is_working is False:
                    is_working = True
                    threading.Thread(target=self.start_orders_thread).start()
                    threading.Thread(target=self.start_light_thread).start()
                    threading.Thread(target=self.start_sensors_thread).start()
        except KeyboardInterrupt:
            self._stop_event.set()

    def start_light_thread(self):
        self.light = Light(self._stop_event, self.config, self.sensors_data)

    def start_orders_thread(self):
        self.orders_client = OrdersClient(self._stop_event, self.config)

    def start_sensors_thread(self):
        self.sensors_client = SensorsClient(self._stop_event, self.config, self.sensors_data)


# Main program logic follows:
if __name__ == '__main__':
    Pyquarium()
