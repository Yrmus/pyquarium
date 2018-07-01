from network.network import Network
from config import Config
import threading
import sched
import time


class ThreadedClient(threading.Thread):

    def __init__(self, stop_event, config: Config):
        threading.Thread.__init__(self)
        self.config = config
        self._stop_event = stop_event
        self._scheduler = sched.scheduler(time.time, time.sleep)
        self._network = Network(config)
        self._scheduler.enter(self.get_scheduler_time(), self.get_scheduler_priority(), self.update)
        self._scheduler.run()

    def update(self):
        if not self._stop_event.is_set():
            self._scheduler.enter(self.get_scheduler_time(), self.get_scheduler_priority(), self.update)

    @staticmethod
    def get_scheduler_time():
        return 2

    @staticmethod
    def get_scheduler_priority():
        return 1
