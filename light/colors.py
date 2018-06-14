class Colors:
    def __init__(self):
        self._sunrise_colors = {
            0: (0, 0, 0,),
            1: (2, 0, 0,),
            2: (5, 0, 0,),
            3: (10, 2, 2,),
            4: (15, 5, 5,),
            5: (15, 10, 5,),
            6: (20, 10, 5,),
            7: (20, 15, 5,),
            8: (20, 20, 5,),
            9: (20, 20, 10,),
            10: (25, 20, 15,),
            11: (25, 20, 20,),
            12: (30, 30, 30,),
            13: (40, 40, 40,),
            14: (50, 50, 50,),
            15: (60, 60, 60,),
            16: (70, 70, 70,),
            17: (80, 80, 80,),
            18: (90, 90, 90,),
            19: (100, 100, 100,),
            20: (110, 110, 110,),
        }

    def get_sunrise_colors_count(self):
        return len(self._sunrise_colors) - 1

    def get_sunrise_colors(self):
        return self._sunrise_colors

    def get_sunrise_color(self, index: int):
        return self._sunrise_colors[index]
