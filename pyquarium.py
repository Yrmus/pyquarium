
from light import Light

class Pyquarium():
    def __init__(self):
        self.light = Light()
        self.start()

    def start(self):
        try:
            while True:
                self.light.set_color(255, 255, 255)
        except KeyboardInterrupt:
            self.light.set_color(0, 0, 0)


# Main program logic follows:
if __name__ == '__main__':
    Pyquarium()
