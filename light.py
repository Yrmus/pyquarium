from neopixel import *
import sched, time
import datetime
from config import Config
from pixels import Pixels


class Light():
    def __init__(self):
        self.config = Config()
        self._pixels = Pixels()
        self._sunrise_time_delta = datetime.timedelta(0, 10)
        self._sunrise_start = datetime.datetime.now()
        self._sunrise_end = self._sunrise_start + self._sunrise_time_delta
        self._sunrise_refresh_time = self._sunrise_time_delta / 255
        self._last_time_action = datetime.datetime.now()
        self._current_color = 0
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.strip = Adafruit_NeoPixel(self._pixels.get_led_count(), self.config.getint('DEFAULT', 'LedPin'),
                                       self.config.getint('DEFAULT', 'LedFreqHz'),
                                       self.config.getint('DEFAULT', 'LedDma'),
                                       self.config.getboolean('DEFAULT', 'LedInvert'),
                                       self.config.getint('DEFAULT', 'LedBrightness'),
                                       self.config.getint('DEFAULT', 'LedChannel'))
        self.strip.begin()

    def update(self, time: datetime):
        if self._sunrise_start < time < self._sunrise_end:
            self._update_sunrise(time)

    def set_color(self, red: int, green: int, blue: int):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(red, green, blue))
        self.strip.show()

    def get_pixel_color(self, index: int):
        return self.parse_color(self.strip.getPixelColor(index))

    def parse_color(self, color: int):
        blue = color & 255
        red = (color >> 8) & 255
        green = (color >> 16) & 255
        return tuple([red, green, blue])

    def hex_to_rgb(self, hex_color: str):
        hex = hex_color.lstrip('#')
        return tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4))

    def get_color_increment(self):
        start_color = self.hex_to_rgb(self.config.get('SUNCYCLE', 'StartColor'))
        end_color = self.hex_to_rgb(self.config.get('SUNCYCLE', 'EndColor'))
        increment = []
        for i in range(0, 3):
            color = end_color[i] - start_color[i]
            increment.append(int(color / self._pixels.get_leds_per_row()))
        return tuple(increment)

    def sunrise(self, time: int):
        time_increment = time / self._pixels.get_leds_per_row()
        schedule_time = 0
        color_increment = self.get_color_increment()
        for led_index in range(self._pixels.get_leds_per_row()):
            self.scheduler.enter(schedule_time + time_increment, 1, self.change_row,
                                 argument=(led_index, color_increment,))
            schedule_time += time_increment
        self.scheduler.run()

    def change_row(self, led_index: int, increment: tuple):
        for pixel_index in self._pixels.get_pixels_for_row(led_index):
            color = self.get_pixel_color(pixel_index)
            if color[0] == 0 and color[1] == 0 and color[2] == 0:
                start_color = self.hex_to_rgb(self.config.get('SUNCYCLE', 'StartColor'))
                self.strip.setPixelColor(pixel_index, Color(start_color[1], start_color[0], start_color[2]))
            else:
                self.strip.setPixelColor(pixel_index, Color(color[1] + increment[1], color[0] + increment[0],
                                                            color[2] + increment[2]))
        self.strip.show()

    def _update_sunrise(self, update_time: datetime):
        if (update_time > (self._last_time_action + self._sunrise_time_delta)) and self._current_color < 255:
            self._current_color = self._current_color + 1
            for row_index in range(self._pixels.get_led_count()):
                for pixel in self._pixels.get_pixels_for_row(row_index):
                    self.strip.setPixelColor(pixel, Color(self._current_color, self._current_color, self._current_color))
                self.strip.show()
