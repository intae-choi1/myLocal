import pyautogui as pag
from pynput.keyboard import Key
import time

class ShiftToggleTask:
    toggle = True
    def __init__(self):
        pass

    def run(self, runner):
        if ShiftToggleTask.toggle:
            runner.press(Key.shift_l)
        else:
            runner.release(Key.shift_l)

        ShiftToggleTask.toggle = not ShiftToggleTask.toggle


class BuffTask1:
    def __init__(self):
        pass

    def run(self, runner):
        runner.press(Key.end, 0.2)
        runner.release(Key.end, 0.1)

        runner.press(Key.delete, 1.1)
        runner.release(Key.delete, 0.1)

        runner.press(Key.shift_l, 0.8)
        runner.release(Key.shift_l)


class BuffTask2:
    def __init__(self):
        pass

    def run(self, runner):
        x, y = pag.locateCenterOnScreen("../imgs/cashop.png", confidence=0.7, region=(0, 800, 1920, 280))
        runner.move_mouse(x, y-110, 0.1)
        runner.click(wait=0.1)

        runner.press(Key.end, 0.2)
        runner.release(Key.end, 0.1)

        runner.press(Key.delete, 0.5)
        runner.release(Key.delete)

        runner.tap(Key.enter)
        runner.type_text("/파티탈퇴")
        runner.tap(Key.enter)


class TellHealTask:
    def __init__(self):
        pass

    def run(self, runner):
        runner.release(Key.shift_l, 0.05)
        runner.tap("c", 0.05)

        runner.press(Key.shift_l, 0.2)
        runner.release(Key.shift_l, 0)


class PressShiftTask:
    def __init__(self):
        pass

    def run(self, runner):
        time.sleep(0.4)
        runner.press(Key.shift_l)


