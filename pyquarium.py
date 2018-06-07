
import sched, time
from light import Light

class Pyquarium():
    def __init__(self):
        self.light = Light()
        self.scheduler = sched.scheduler(time.time, time.sleep)

        self.start()

    def start(self):
        try:
            is_working = False
            while True:
                if is_working is False:
                    is_working = True
                    self.scheduler.enter(1, 1, self.update_light_status)
                    self.scheduler.run()
        except KeyboardInterrupt:
            self.light.set_color(0, 0, 0)

    def update_light_status(self):
        self.light.update()
        self.scheduler.enter(1, 1, self.update_light_status)
        self.scheduler.run()


# Main program logic follows:
if __name__ == '__main__':
    Pyquarium()
