import time
from pynput import keyboard, mouse
from pynput.keyboard import Key
from pynput.mouse import Button

from utils.interrupt_sleep import interruptible_sleep


class ActionRunner:
    def __init__(self, stop_controller):
        self.stop_controller = stop_controller
        self.keyboard = keyboard.Controller()
        self.mouse = mouse.Controller() 

    # 내부 중단 체크
    def _check(self):
        self.stop_controller.raise_if_stopped()

    # 대기
    def wait(self, seconds):
        interruptible_sleep(seconds, self._check)

    def press(self, key, wait=0):
        self._check()
        self.keyboard.press(key)
        self.wait(wait)

    def release(self, key, wait=0):
        self._check()
        self.keyboard.release(key)
        self.wait(wait)

    def tap(self, key, wait=0.25):
        self._check()
        self.keyboard.tap(key)
        self.wait(wait)

    # 마우스 이동
    def move_mouse(self, x, y, wait=0.04):
        self._check()
        self.mouse.position = (x, y)
        self.wait(wait)

    # 클릭
    def click(self, button=mouse.Button.left, count=1, wait=0.04):
        self._check()
        self.mouse.click(button, count)
        self.wait(wait)

    # 더블클릭
    def double_click(self):
        self.click(count=2)

    # 휠
    def scroll(self, dx=0, dy=0, wait=0.04):
        self._check()
        self.mouse.scroll(dx=dx, dy=dy)
        self.wait(wait)
    
    # 드래그
    def mouse_drag(self, sx, sy, ex, ey, gap=0.05):
        self._check()
        self.mouse.position = (sx, sy)
        self.wait(gap)
        self.mouse.press(Button.left)
        self.wait(gap)
        self.mouse.position = (ex, ey)
        self.wait(gap)
        self.mouse.release(Button.left)
        self.wait(gap)

    def type_text(self, text):
        self._check()
        self.keyboard.type(text)

    # 단축키
    def hotkey(self, modifier, key):
        self._check()

        with self.keyboard.pressed(modifier):

            self.keyboard.press(key)
            self.keyboard.release(key)

