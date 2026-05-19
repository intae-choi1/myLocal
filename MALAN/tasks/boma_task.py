from datetime import datetime, timedelta

from pynput.keyboard import Key


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


class JumpSkillTask:
    def __init__(self, char):
        self.char = char

    def run(self, runner):
        runner.tap(self.char)
        runner.tap(Key.space)
