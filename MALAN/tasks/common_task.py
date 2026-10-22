import random, time
from datetime import datetime, timedelta

import mss
import pyautogui as pag
import numpy as np
import pygetwindow as gw
from pynput.keyboard import Key


sct = mss.mss()


class ChannelChangeTask:
    def __init__(self):
        pass

    def run(self, runner):
        # self.do_origin(runner)
        self.do_special(runner)
    
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
        n = 7
        top = 526 + (10-n) * 21
        # monitor = {"left": 846, "top": 610, "width": 1, "height": 1} # 채널 10줄안되면 수정해서 사용 6줄일때 846,610
        monitor = {"left": 846, "top": top, "width": 1, "height": 1} 
        while not runner.stop_controller.is_stopped():
            runner.tap(Key.esc, 0.1)
            runner.tap(Key.enter, 0.4)
            runner.tap(Key.right, 0.2)
            img = sct.grab(monitor)
            color = img.pixel(0, 0)  # (R, G, B)
            print(color)
            if np.all(np.array(color) -np.array((204, 204, 187)) < 10):
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
        nx = 975 + 70 * 3       # ※※채널 x방향 n번째 ※※
        ny = 550 + 21 * 10  # ※※채널 y방향 n번째 ※※
        while not runner.stop_controller.is_stopped():
            rx = random.randrange(0, 50)
            ry = random.randrange(0, 11)
            
            runner.tap(Key.esc, 0.1)
            runner.tap(Key.enter, 0.4)

            runner.move_mouse(nx+rx, ny+ry, 0)    # ※※채널※※
            runner.click()
            
            runner.tap(Key.enter, 0.1)
            runner.tap(Key.esc, 0.1)


    def do_special(self, runner):
        monitor = {"left": 1100, "top": 585, "width": 1, "height": 1}
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
        runner.release(Key.space, 0.04)
        runner.release(Key.right, 0.04)

        runner.press(Key.left, 0.04)
        runner.press("x", 0.02)
        runner.release("x", 0.06)
        runner.release(Key.left, 0.04)


class LDPTask:
    def __init__(self, num):
        self.num = num
        pass

    def run(self, runner):
        if self.num < 3:
            self.activate_window("토르쿠")
            runner.press(Key.shift_l, 0.05)
            runner.release(Key.shift_l, 0.05)
            if self.num == 2:
                runner.press("c", 0.05)
                runner.release("c", 0.05)

            self.activate_window("MapleStory Worlds")

        elif self.num == 3:
            runner.press("[", 0.1)
            runner.release("[", 0.05)
            x, y = pag.locateCenterOnScreen(f"../imgs/party_symbol.png", confidence=0.75)
            x1, y1 = x, y+190
            x2, y2 = x+400, y+95
            runner.mouse_drag(x1, y1, x2, y2, 0.1)
            runner.wait(1)

            self.activate_window("흣구리")
            runner.press("r", 0.1)
            runner.release("r", 0.05)
            self.activate_window("MapleStory Worlds")
            runner.wait(0.8)
            runner.mouse_drag(x2, y2, x1, y1, 0.1)


    def activate_window(self, title):
        windows = gw.getWindowsWithTitle(title)
        if windows:
            win = windows[0]

            # 최소화되어 있다면 복원
            if win.isMinimized:
                win.restore()

            # 창 활성화
            win.activate()

            # print(f"활성화 완료: {win.title}")
        else:
            print("해당 프로그램을 찾을 수 없습니다.")
