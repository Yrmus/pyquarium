from light.light import Light
import threading


class Pyquarium:
    def __init__(self):
        self._light_stop_event = threading.Event()
        self.light = None
        self.start()

    def start(self):
        try:
            is_working = False
            while True:
                if is_working is False:
                    is_working = True
                    threading.Thread(target=self.start_light_thread).start()
        except KeyboardInterrupt:
            self._light_stop_event.set()

    def start_light_thread(self):
        self.light = Light(self._light_stop_event)


# Main program logic follows:
if __name__ == '__main__':
    Pyquarium()
