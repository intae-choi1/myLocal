import threading


class StopController:
    def __init__(self):
        self.stop_event = threading.Event()


    def stop(self):
        self.stop_event.set()


    def reset(self):
        self.stop_event.clear()


    def is_stopped(self):
        return self.stop_event.is_set()


    def raise_if_stopped(self):
        if self.is_stopped():
            raise InterruptedError("자동화 중단")