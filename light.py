from neopixel import *
import datetime
from config import Config
from pixels import Pixels


class Light():
    def __init__(self, ):
        self.config = Config()
        self._pixels = Pixels()
        self.sunrise_time = self.config.get('SUNCYCLE', 'Sunrise')
        self.sunset_time = self.config.get('SUNCYCLE', 'Sunset')
        self.is_shining = False
        self.strip = Adafruit_NeoPixel(self._pixels.get_led_count(), self.config.getint('DEFAULT', 'LedPin'),
                                       self.config.getint('DEFAULT', 'LedFreqHz'),
                                       self.config.getint('DEFAULT', 'LedDma'),
                                       self.config.getboolean('DEFAULT', 'LedInvert'),
                                       self.config.getint('DEFAULT', 'LedBrightness'),
                                       self.config.getint('DEFAULT', 'LedChannel'))
        self.strip.begin()

    def update(self):
        now = datetime.datetime.now()
        if now > Light.get_time(self.sunrise_time) and not self.is_shining:
            self.set_color(100, 100, 100)
        if now > Light.get_time(self.sunset_time) and self.is_shining:
            self.set_color(0, 0, 0)

    def set_color(self, red: int, green: int, blue: int):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(red, green, blue))
        self.strip.show()

    def get_pixel_color(self, index: int):
        return self.parse_color(self.strip.getPixelColor(index))

    @staticmethod
    def parse_color(color: int):
        blue = color & 255
        red = (color >> 8) & 255
        green = (color >> 16) & 255
        return tuple([red, green, blue])

    @staticmethod
    def hex_to_rgb(hex_color: str):
        stripped_hex = hex_color.lstrip('#')
        return tuple(int(stripped_hex[i:i + 2], 16) for i in (0, 2, 4))

    @staticmethod
    def get_time(time_string: str):
        time_now = datetime.datetime.now()
        splited = time_string.split(':')
        return time_now.replace(hour=int(splited[0]), minute=int(splited[1]))
