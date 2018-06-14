from neopixel import *
from config import Config
from light.pixels import Pixels


class LedStrip:
    def __init__(self):
        self.config = Config()
        self._pixels = Pixels()
        self.strip = Adafruit_NeoPixel(self._pixels.get_led_count(), self.config.getint('DEFAULT', 'LedPin'),
                                       self.config.getint('DEFAULT', 'LedFreqHz'),
                                       self.config.getint('DEFAULT', 'LedDma'),
                                       self.config.getboolean('DEFAULT', 'LedInvert'),
                                       self.config.getint('DEFAULT', 'LedBrightness'),
                                       self.config.getint('DEFAULT', 'LedChannel'))
        self.strip.begin()

    def set_pixel_color(self, pixel_index: int, red: int, green: int, blue: int):
        # print(pixel_index, red, green, blue)
        self.strip.setPixelColor(pixel_index, Color(green, red, blue))

    def show(self):
        # print('show')
        self.strip.show()

    def get_pixel_color(self, index: int):
        # print('get pixel color')
        # return index, index, index
        return LedStrip.parse_color(self.strip.getPixelColor(index))

    def set_color(self, red: int, green: int, blue: int):
        for i in range(self._pixels.get_led_count()):
            self.set_pixel_color(i, red, green, blue)

    def update_color(self, red: int, green: int, blue: int):
        self.set_color(red, green, blue)
        self.show()

    def update_row_color(self, row_index: int, red: int, green: int, blue: int):
        self.set_row_color(row_index, red, green, blue)
        self.show()

    def set_row_color(self, row_index: int, red: int, green: int, blue: int):
        for pixel in self._pixels.get_pixels_for_row(row_index):
            self.set_pixel_color(pixel, red, green, blue)

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
