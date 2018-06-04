from neopixel import *
import sched, time
from config import Config


class Light():
    def __init__(self):
        self.config = Config()
        self.leds_per_row = self.config.getint('DEFAULT', 'LedsPerRow')
        self.led_rows = self.config.getint('DEFAULT', 'LedRows')
        self.scheduler = sched.scheduler(time.time, time.sleep)
        led_count = self.led_rows * self.leds_per_row
        self.strip = Adafruit_NeoPixel(led_count, self.config.getint('DEFAULT', 'LedPin'),
                                       self.config.getint('DEFAULT', 'LedFreqHz'),
                                       self.config.getint('DEFAULT', 'LedDma'),
                                       self.config.getboolean('DEFAULT', 'LedInvert'),
                                       self.config.getint('DEFAULT', 'LedBrightness'),
                                       self.config.getint('DEFAULT', 'LedChannel'))
        self.strip.begin()

    def set_color(self, red: int, green: int, blue: int):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(red, green, blue))
        self.strip.show()
        for i in range(self.strip.numPixels()):
            print('led', i, ' ', self.get_pixel_color(i))

    def get_pixel_color(self, index: int):
        return self.parse_color(self.strip.getPixelColor(index))

    def parse_color(self, color: int):
        binary = bin(color)
        blue = color & 255
        green = (color >> 8) & 255
        red = (color >> 16) & 255
        return red, green, blue
        return tuple(int(binary[i:i + 8], 2) for i in [2, 10, 18])

    def hex_to_rgb(self, hex_color: str):
        hex = hex_color.lstrip('#')
        return tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4))

    def get_color_increment(self):
        start_color = self.hex_to_rgb(self.config.get('SUNCYCLE', 'StartColor'))
        end_color = self.hex_to_rgb(self.config.get('SUNCYCLE', 'EndColor'))
        increment = []
        for i in range(0, 3):
            increment.append(end_color[i] - start_color[i])
        return tuple(increment)

    def sunrise(self, time: int):
        time_increment = time / self.leds_per_row
        schedule_time = 0
        color_increment = self.get_color_increment()
        for led_index in range(self.leds_per_row):
            self.scheduler.enter(schedule_time + time_increment, 1, self.change_row,
                                 argument=(led_index, color_increment,))
            schedule_time += time_increment
        self.scheduler.run()

    def change_row(self, led_index: int, increment: tuple):
        for row_index in range(self.led_rows):
            pixel_index = led_index + (row_index * self.leds_per_row)
            color = self.get_pixel_color(pixel_index)
            self.strip.setPixelColor(pixel_index, Color(color[0] + increment[0], color[1] + increment[1],
                                                        color[2] + increment[2]))
        self.strip.show()
