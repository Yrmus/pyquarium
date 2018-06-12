import datetime
from config import Config
from light.pixels import Pixels
from light.colors import Colors
from light.led_strip import LedStrip


class Light:
    def __init__(self, ):
        self.config = Config()
        self.led_strip = LedStrip()
        self._pixels = Pixels()
        self._colors = Colors()
        self._sunrise_time = self.config.get('SUNCYCLE', 'Sunrise')
        self._sunset_time = self.config.get('SUNCYCLE', 'Sunset')
        self.is_shining = False

    def update(self):
        now = datetime.datetime.now()
        if now > Light.get_time(self._sunrise_time) and not self.is_shining:
            self.led_strip.update_color(100, 100, 100)
        if now > Light.get_time(self._sunset_time) and self.is_shining:
            self.led_strip.update_color(0, 0, 0)

    @staticmethod
    def get_time(time_string: str):
        time_now = datetime.datetime.now()
        splited = time_string.split(':')
        return time_now.replace(hour=int(splited[0]), minute=int(splited[1]))
