from datetime import datetime, timedelta

from pynput.keyboard import Key


class ShiftToggleTask:
    toggle = True
    def __init__(self):
        pass

    def run(self, runner):
        self.do_origin(runner)
        # self.do_special(runner)
        # self.do_special2(runner)
    
    def do_origin(self, runner):
        while not runner.stop_controller.is_stopped():
            runner.press(Key.shift_l)
            runner.wait(51)
            runner.release(Key.shift_l)

    def do_special(self, runner):
        i = 0
        while not runner.stop_controller.is_stopped():
            if i == 0 or i%3==0:
                runner.press("e")
                runner.wait(0.3)
                runner.release("e")
                runner.wait(0.51)
            i+=1
            runner.press(Key.shift_l)
            runner.wait(47.5)
            runner.release(Key.shift_l)
            runner.wait(0.55)

            runner.press(Key.right)
            runner.wait(0.13)
            runner.release(Key.right)
            runner.wait(0.45)

            runner.press(Key.shift_l)
            runner.wait(0.6)
            runner.release(Key.shift_l)
            runner.wait(0.55)
            
            runner.press(Key.left)
            runner.wait(0.1)
            runner.release(Key.left)
            runner.wait(0.45)

    def do_special2(self, runner):
        while not runner.stop_controller.is_stopped():
            runner.press(Key.shift_l)
            runner.wait(0.4)
            runner.release(Key.shift_l)
            runner.wait(6)

    def do_final(self, runner):
        runner.keyboard.release(Key.shift_l)


class JumpSkillTask:
    def __init__(self, char):
        self.char = char

    def run(self, runner):
        # runner.tap(self.char)
        # runner.tap(Key.space)
        runner.keyboard.tap(self.char)
        runner.keyboard.tap(Key.space)
