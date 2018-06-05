from config import Config


class Pixels:
    def __init__(self):
        self.config = Config()
        self.leds_per_row = self.config.getint('DEFAULT', 'LedsPerRow')
        self.led_rows = self.config.getint('DEFAULT', 'LedRows')
        self.pixels_by_row = self._prepare_pixels_by_row()
        print(self.pixels_by_row)

    def get_pixels_for_row(self, row: int):
        if row >= self.leds_per_row:
            row = self.leds_per_row - 1

    def _prepare_pixels_by_row(self):
        rows_dict = {}
        for row_index in range(self.leds_per_row):
            row_pixels = tuple()
            if row_index % 2 == 0:
                row_beginning_index = row_index * self.leds_per_row
                remove_to_progress = False
            else:
                row_beginning_index = ((row_index + 1) * self.leds_per_row) - 1
                remove_to_progress = True

            for index in range(self.led_rows):
                if remove_to_progress:
                    pixel_index = row_beginning_index - index
                else:
                    pixel_index = index + row_beginning_index
                row_pixels = row_pixels + (pixel_index, )

            rows_dict[str(row_index)] = row_pixels
        return rows_dict
