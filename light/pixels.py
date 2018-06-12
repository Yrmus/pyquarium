from config import Config


class Pixels:
    def __init__(self):
        self.config = Config()
        self._leds_per_row = self.config.getint('DEFAULT', 'LedsPerRow')
        self._led_rows = self.config.getint('DEFAULT', 'LedRows')
        self.pixels_by_row = self._prepare_pixels_by_row()

    def get_leds_per_row(self):
        return self._leds_per_row

    def get_led_rows(self):
        return self._led_rows

    def get_led_count(self):
        return self._led_rows * self._leds_per_row

    def get_pixels_for_row(self, row: int):
        return self.pixels_by_row[str(row)]

    def _prepare_pixels_by_row(self):
        rows_dict = {}
        for row_index in range(self._leds_per_row):
            row_pixels = tuple()
            for index in range(self._led_rows):
                if index % 2 == 0:
                    pixel_index = (index * self._leds_per_row) + row_index
                else:
                    pixel_index = (((index + 1) * self._leds_per_row) - 1) - row_index
                row_pixels = row_pixels + (pixel_index,)

            rows_dict[str(row_index)] = row_pixels
        return rows_dict
