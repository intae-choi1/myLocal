import time
from pynput import keyboard, mouse
from pynput.keyboard import Key

from utils.interrupt_sleep import interruptible_sleep


class ActionRunner:
    def __init__(self, stop_controller):
        self.stop_controller = stop_controller

        self.keyboard = keyboard.Controller()

        self.mouse = mouse.Controller()

        self.is_typing = False


    # 내부 중단 체크
    def _check(self):
        self.stop_controller.raise_if_stopped()


    # 대기
    def wait(self, seconds):
        interruptible_sleep(seconds, self._check)


    def press(self, key, wait=0):
        self._check()
        # self.is_typing = True
        self.keyboard.press(key)
        time.sleep(wait)

    def release(self, key, wait=0):
        self._check()
        self.keyboard.release(key)
        # self.is_typing = False
        time.sleep(wait)

    def tap(self, key, wait=0.25):
        self._check()
        self.keyboard.tap(key)
        time.sleep(wait)


    # 마우스 이동
    def move_mouse(self, x, y, wait=0.04):
        self._check()
        self.mouse.position = (x, y)
        time.sleep(wait)


    # 클릭
    def click(self, button=mouse.Button.left, count=1, wait=0.04):
        self._check()
        self.mouse.click(button, count)
        time.sleep(wait)


    # 더블클릭
    def double_click(self):
        self.click(count=2)


    # 텍스트 입력
    def type_text(self, text):
        self._check()
        self.is_typing = True

        try:
            self.keyboard.type(text)

        finally:
            self.is_typing = False


    # 단축키
    def hotkey(self, modifier, key):
        self._check()

        with self.keyboard.pressed(modifier):

            self.keyboard.press(key)
            self.keyboard.release(key)

