import datetime
import sched
import threading
import time

from config import Config
from light.colors import Colors
from light.led_strip import LedStrip
from light.pixels import Pixels
from sensors_data import SensorsData


class Light(threading.Thread):
    STATE_DAWN = 0
    STATE_SUNRISE = 1
    STATE_DAY = 2
    STATE_SUNSET = 3
    STATE_DUSK = 4

    def __init__(self, stop_event, config: Config, sensors_data: SensorsData):
        threading.Thread.__init__(self)
        self.sensors_data = sensors_data
        self._stop_event = stop_event
        self.config = config
        self.led_strip = LedStrip(config)
        self._pixels = Pixels()
        self._colors = Colors()
        self._scheduler = sched.scheduler(time.time, time.sleep)

        self._sunrise_time = self.config.get('SUNCYCLE', 'Sunrise')
        self._sunset_time = self.config.get('SUNCYCLE', 'Sunset')

        self._day_effect_duration = max(int(self.config.getint('SUNCYCLE', 'DayEffectDuration')),
                                        self._colors.get_sunrise_colors_count() + self._pixels.get_leds_per_row())
        self._progress_per_update = max(int(
            self._day_effect_duration / (self._colors.get_sunrise_colors_count() + self._pixels.get_leds_per_row())), 1)

        self.state = self.STATE_DAWN
        self.sensors_data.day_time = self.state
        self._effect_progress = 0
        self._last_shining_row = 0
        self._row_colors = {}

        self._last_check_date = datetime.datetime.today().date()
        self._scheduler.enter(10, 1, self.update)
        self._scheduler.run()

    def update(self):
        self._sunrise_time = self.config.get('SUNCYCLE', 'Sunrise')
        self._sunset_time = self.config.get('SUNCYCLE', 'Sunset')
        self.check_for_date_change()
        if self.is_time_to_sunrise():
            self.led_strip.update_color(*self._colors.get_sunrise_color(0))
            self._initialize_day_effect(self.STATE_SUNRISE)
        elif self.is_time_to_sunset():
            self.led_strip.update_color(*self._colors.get_sunrise_color(self._colors.get_sunrise_colors_count()))
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
        return now > Light.get_time(self._sunrise_time) and self.state == self.STATE_DAWN

    def is_time_to_sunset(self):
        now = datetime.datetime.now()
        return now > Light.get_time(self._sunset_time) and self.state == self.STATE_DAY

    def is_time_to_update(self):
        return self._effect_progress <= self._day_effect_duration

    def _initialize_day_effect(self, direction: int):
        if direction == self.STATE_SUNRISE:
            self.change_state(self.STATE_SUNRISE)
            print('Sunrise started')
        elif direction == self.STATE_SUNSET:
            self.change_state(self.STATE_SUNSET)
            print('Sunset started')
        else:
            raise ValueError('Day effect %d unknown' % direction)
        self.sensors_data.day_time = self.state

    def _update(self):
        # Do nothing at day or night
        if self.state in [self.STATE_DAWN, self.STATE_DAY, self.STATE_DUSK]:
            print('day or night')
            return
        if self.is_time_to_update():
            rows_done = 0
            # Perform actions only with proper interval
            if self._effect_progress % self._progress_per_update == 0:
                # Sunrise
                if self.state == self.STATE_SUNRISE:
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

                    if rows_done == self._pixels.get_leds_per_row():
                        self.change_state(Light.STATE_DAY)
                    print('sunrise update')
                # Sunset
                elif self.state == self.STATE_SUNSET:
                    for pixel_index in range(self._last_shining_row):
                        index_key = str(pixel_index)
                        if index_key not in self._row_colors:
                            self._row_colors[index_key] = self._colors.get_sunrise_colors_count()
                        current_row_color = self._row_colors[index_key]
                        if current_row_color == 0:
                            rows_done += 1
                            continue
                        new_row_color = current_row_color - 1
                        self.led_strip.set_row_color(pixel_index, *self._colors.get_sunrise_color(new_row_color))
                        self._row_colors[index_key] = new_row_color
                    self.led_strip.show()

                    if rows_done == self._pixels.get_leds_per_row():
                        self.change_state(Light.STATE_DUSK)
                    print('sunset update')

                if self._last_shining_row < self._pixels.get_leds_per_row():
                    self._last_shining_row += 1
                self._effect_progress += 1

    def change_state(self, state: int):
        print('state changed')
        self.state = state
        self.sensors_data.day_time = state
        self._effect_progress = 0
        self._last_shining_row = 0
        self._row_colors = {}

    def check_for_date_change(self):
        if datetime.datetime.today().date() > self._last_check_date and self.state == self.STATE_DUSK:
            self.change_state(self.STATE_DAWN)
            self._last_check_date = datetime.datetime.today().date()
