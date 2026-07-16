import random, time
from datetime import datetime, timedelta

import mss
import pyautogui as pag
from pynput.keyboard import Key


sct = mss.mss()


class ChannelChangeTask:
    def __init__(self):
        pass

    def run(self, runner):
        self.do_origin(runner)
        # self.do_special(runner)
    
    def do_origin(self, runner):
        nx = 710 + 140 * 1       # ※※채널 x방향 n번째 ※※
        ny = 490 + 42 * 10  # ※※채널 y방향 n번째 ※※
        while not runner.stop_controller.is_stopped():
            rx = random.randrange(0, 80)
            ry = random.randrange(0, 21)
            
            runner.tap(Key.esc, 0.1)
            runner.tap(Key.enter, 0.4)

            runner.move_mouse(nx+rx, ny+ry, 0)    # ※※채널※※
            runner.click()
            
            runner.tap(Key.enter, 0.1)
            runner.tap(Key.esc, 0.1)


    def do_special(self, runner):
        monitor = {"left": 950, "top": 550, "width": 1, "height": 1}
        # monitor = {"left": xx, "top": yy, "width": 1, "height": 1} # 채널 10줄안되면 수정해서 사용
        while not runner.stop_controller.is_stopped():
            runner.tap(Key.esc, 0.1)
            runner.tap(Key.enter, 0.4)
            runner.tap(Key.right, 0.2)
            img = sct.grab(monitor)
            color = img.pixel(0, 0)  # (R, G, B)
            if color == (221, 221, 221):
                runner.tap(Key.enter, 0.1)
                print("채널찾기종료")
                break
                # runner.tap(Key.esc, 0.5)
            else:
                runner.tap(Key.esc, 0.2)


class NotebookChannelChangeTask:
    def __init__(self):
        pass

    def run(self, runner):
        self.do_origin(runner)
        # self.do_special(runner)
    
    def do_origin(self, runner):
        nx = 710 + 140 * 1       # ※※채널 x방향 n번째 ※※
        ny = 490 + 42 * 10  # ※※채널 y방향 n번째 ※※
        while not runner.stop_controller.is_stopped():
            rx = random.randrange(0, 80)
            ry = random.randrange(0, 21)
            
            runner.tap(Key.esc, 0.1)
            runner.tap(Key.enter, 0.4)

            runner.move_mouse(nx+rx, ny+ry, 0)    # ※※채널※※
            runner.click()
            
            runner.tap(Key.enter, 0.1)
            runner.tap(Key.esc, 0.1)


    def do_special(self, runner):
        monitor = {"left": 950, "top": 550, "width": 1, "height": 1}
        # monitor = {"left": xx, "top": yy, "width": 1, "height": 1} # 채널 10줄안되면 수정해서 사용
        while not runner.stop_controller.is_stopped():
            runner.tap(Key.esc, 0.1)
            runner.tap(Key.enter, 0.4)
            runner.tap(Key.right, 0.2)
            img = sct.grab(monitor)
            color = img.pixel(0, 0)  # (R, G, B)
            if color == (221, 221, 221):
                runner.tap(Key.enter, 0.1)
                print("채널찾기종료")
                break
                # runner.tap(Key.esc, 0.5)
            else:
                runner.tap(Key.esc, 0.2)


class FlJumpTask:
    def __init__(self):
        pass

    def run(self, runner):
        runner.press(Key.right, 0.04)
        runner.press(Key.space, 0.04)
        runner.release(Key.space, 0.03)
        runner.release(Key.right, 0.03)

        runner.press(Key.left, 0.04)
        runner.press("x", 0.02)
        runner.release("x", 0.06)
        runner.release(Key.left, 0.04)