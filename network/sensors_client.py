from config import Config
from network.threaded_client import ThreadedClient
from sensors_data import SensorsData


class SensorsClient(ThreadedClient):

    def __init__(self, stop_event, config: Config, sensors_data: SensorsData):
        self._sensors_data = sensors_data
        ThreadedClient.__init__(self, stop_event, config)

    def update(self):
        self._network.post_sensors_data(self._sensors_data)
        super(SensorsClient, self).update()

    @staticmethod
    def get_scheduler_time():
        # Ten minutes interval is enough
        return 60 * 10
