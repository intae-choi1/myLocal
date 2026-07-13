import time

import cv2
import mss
import numpy as np
import pyautogui as pag
# from ultralytics import YOLO
from pynput.keyboard import Key


sct = mss.mss()


class ShiftToggleTask:
    toggle = True
    def __init__(self):
        pass

    def run(self, runner):
        # if ShiftToggleTask.toggle:
        #     runner.press(Key.shift_l)
        # else:
        #     runner.release(Key.shift_l)

        # ShiftToggleTask.toggle = not ShiftToggleTask.toggle
        while not runner.stop_controller.is_stopped():
            runner.press(Key.shift_l)
            runner.wait(45.5)
            runner.release(Key.shift_l)
            runner.wait(0.55)

            runner.press(Key.left)
            runner.wait(0.1)
            runner.release(Key.left)
            runner.wait(0.55)

            runner.press(Key.shift_l)
            runner.wait(1.5)
            runner.release(Key.shift_l)
            runner.wait(0.55)
            
            runner.press(Key.right)
            runner.wait(0.1)
            runner.release(Key.right)
            runner.wait(0.55)

    def final_do(self, runner):
        runner.keyboard.release(Key.shift_l)


class ShiftWhileTask:
    def __init__(self):
        pass

    def run(self, runner):
        while not runner.stop_controller.is_stopped():
            runner.press(Key.shift_l)
            runner.wait(3)
            runner.release(Key.shift_l)
            runner.wait(4)
    
    def final_do(self, runner):
        runner.keyboard.release(Key.shift_l)


class CentaurShiftTask:
    is_pressed_shift = False
    # model = YOLO("best_redcen.pt")
    def __init__(self):
        self.monitor = {
            # "top": 500,
            "top": 550,
            "left": 700,
            "height": 420,
            "width": 920,
        }

    def run(self, runner):
        no_detection_count = 0
        while not runner.stop_controller.is_stopped():
            # 스크린샷
            screenshot = np.array(sct.grab(self.monitor))
            # BGR 변환
            frame = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
            # YOLO 추론
            results = CentaurShiftTask.model(frame, verbose=False, conf=0.35)

            # annotated_frame = results[0].plot()
            find = len(results[0].boxes)
            # print(f"{find=}")
            # print(f"{no_detection_count=}")

            if find:
                no_detection_count = 0
                if CentaurShiftTask.is_pressed_shift:
                    continue
                CentaurShiftTask.is_pressed_shift = True
                runner.press(Key.shift_l)
            else:
                no_detection_count += 1

            if no_detection_count >= 3:
                no_detection_count = 0
                CentaurShiftTask.is_pressed_shift = False
                runner.release(Key.shift_l)
            
            time.sleep(0.1)

        else:
            print("centaur종료")
            if CentaurShiftTask.is_pressed_shift:
                no_detection_count = 0
                CentaurShiftTask.is_pressed_shift = False
                runner.release(Key.shift_l)


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

        runner.press(Key.delete, 1.5)
        runner.release(Key.delete, 0.1)

        # runner.press(Key.shift_l, 0.8)
        # runner.release(Key.shift_l)

        runner.tap(Key.enter)
        runner.type_text("/파티탈퇴")
        runner.tap(Key.enter)


class TellHealTask:
    def __init__(self):
        pass

    def run(self, runner):
        runner.release(Key.shift_l, 0.05)
        # runner.tap("x", 0.05)

        # runner.press(Key.shift_l, 0.15)
        # runner.release(Key.shift_l, 0)


class PressShiftTask:
    def __init__(self):
        pass

    def run(self, runner):
        time.sleep(0.4)
        runner.press(Key.shift_l)


