import datetime
import sched
import threading
import time

from config import Config
from light.colors import Colors
from light.led_strip import LedStrip
from light.pixels import Pixels


class Light(threading.Thread):
    STATE_NIGHT = 0
    STATE_SUNRISE = 1
    STATE_DAY = 2
    STATE_SUNSET = 3

    def __init__(self, stop_event):
        threading.Thread.__init__(self)
        self._stop_event = stop_event
        self.config = Config()
        self.led_strip = LedStrip()
        self._pixels = Pixels()
        self._colors = Colors()
        self._scheduler = sched.scheduler(time.time, time.sleep)

        self._sunrise_time = self.config.get('SUNCYCLE', 'Sunrise')
        self._sunset_time = self.config.get('SUNCYCLE', 'Sunset')

        self._day_effect_duration = max(int(self.config.getint('SUNCYCLE', 'DayEffectDuration')),
                                        self._colors.get_sunrise_colors_count() + self._pixels.get_leds_per_row())
        self._progress_per_update = max(int(
            self._day_effect_duration / (self._colors.get_sunrise_colors_count() + self._pixels.get_leds_per_row())), 1)
        self._effect_progress = 0
        self._last_shining_row = 0
        self._row_colors = {}

        self.state = self.STATE_NIGHT
        self._scheduler.enter(1, 1, self.update)
        self._scheduler.run()

    def update(self):
        if self.is_time_to_sunrise():
            self._initialize_day_effect(self.STATE_SUNRISE)
        elif self.is_time_to_sunset():
            self._initialize_day_effect(self.STATE_SUNSET)
        self._update()
        if not self._stop_event.is_set():
            self._scheduler.enter(1, 1, self.update)
        else:
            self.led_strip.update_color(0, 0, 0)

    @staticmethod
    def get_time(time_string: str):
        time_now = datetime.datetime.now()
        splited = time_string.split(':')
        return time_now.replace(hour=int(splited[0]), minute=int(splited[1]), second=0)

    def is_time_to_sunrise(self):
        now = datetime.datetime.now()
        return now > Light.get_time(self._sunrise_time) and self.state == self.STATE_NIGHT

    def is_time_to_sunset(self):
        now = datetime.datetime.now()
        return now > Light.get_time(self._sunset_time) and self.state == self.STATE_DAY

    def is_time_to_update(self):
        return self._effect_progress <= self._day_effect_duration

    def _initialize_day_effect(self, direction: int):
        self._effect_progress = 0
        if direction == self.STATE_SUNRISE:
            self.state = self.STATE_SUNRISE
            print('Sunrise started')
        elif direction == self.STATE_SUNSET:
            self.state = self.STATE_SUNSET
            print('Sunset started')
        else:
            raise ValueError('Day effect %d unknown' % direction)

    def _update(self):
        # Do nothing at day or night
        if self.state == self.STATE_NIGHT or self.state == self.STATE_DAY:
            print('day or night')
            return
        if self.is_time_to_update():
            rows_done = 0
            if self.state == self.STATE_SUNRISE and self._effect_progress % self._progress_per_update == 0:
                for pixel_index in range(self._last_shining_row):
                    index_key = str(pixel_index)
                    if index_key not in self._row_colors:
                        self._row_colors[index_key] = 0
                    current_row_color = self._row_colors[index_key]
                    if current_row_color == self._colors.get_sunrise_colors_count():
                        rows_done += 1
                        continue
                    new_row_color = current_row_color + 1
                    self.led_strip.set_row_color(pixel_index, *self._colors.get_sunrise_color(new_row_color))
                    self._row_colors[index_key] = new_row_color
                self.led_strip.show()
                if self._last_shining_row < self._pixels.get_leds_per_row():
                    self._last_shining_row += 1
                if rows_done == self._pixels.get_leds_per_row():
                    self.change_state(Light.STATE_DAY)
                print('sunrise update')
            else:
                print('sunset update')
            self._effect_progress += 1

    def change_state(self, state: int):
        print('state changed')
        self.state = state
        self._effect_progress = 0
        self._last_shining_row = 0
        self._row_colors = {}
