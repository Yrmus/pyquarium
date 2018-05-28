from neopixel import *
import ConfigParser


#
# LED_COUNT = 105  # Number of LED pixels.
# LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
# LED_DMA = 10  # DMA channel to use for generating signal (try 10)
# LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
# LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
# LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53


class Light():
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read('config.ini')
        # defaultConfig = config['DEFAULT']
        self.strip = Adafruit_NeoPixel(config.getint('DEFAULT', 'LedCount'), config.getint('DEFAULT', 'LedPin'),
                                       config.getint('DEFAULT', 'LedFreqHz'), config.getint('DEFAULT', 'LedDma'),
                                       config.getboolean('DEFAULT', 'LedInvert'), config.getint('DEFAULT', 'LedBrightness'),
                                       config.getint('DEFAULT', 'LedChannel'))
        self.strip.begin()

    def set_color(self, red, green, blue):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(red, green, blue))
        self.strip.show()

    def turn_off(self):
        pass
