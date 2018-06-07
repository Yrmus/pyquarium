
import datetime
from light import Light
import queue

class Pyquarium():
    def __init__(self):
        self.light = Light()
        self.working = False
        self.start()

    def start(self):
        thread_queue = queue.Queue()
        try:
            is_working = False
            while True:
                # self.light.update(datetime.datetime.now())
                if is_working is False:
                    is_working = True
                    Light(thread_queue).start()
                    thread_queue.put('s')
                # if not self.light.is_working():
                #     self.light.start()
                # if not self.working:
                #
                #     print('starting')
                #     self.light.sunrise(30)
                #     # self.light.set_color(255, 255, 255)
                #     self.working = True
        except KeyboardInterrupt:
            thread_queue.put(None)
            self.light.set_color(0, 0, 0)


# Main program logic follows:
if __name__ == '__main__':
    Pyquarium()
