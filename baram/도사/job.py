import time, random

import pyautogui as pag
from pynput.keyboard import Key


######################### 조합 키 #########################
# 부활
def revive(event, lock, controller, stores, combis, physics, key):
    time.sleep(random.uniform(0.03, 0.04))
    controller.tap(Key.esc)
    time.sleep(random.uniform(0.03, 0.04))
    controller.press(Key.shift)
    time.sleep(random.uniform(0.03, 0.04))
    controller.tap('z')
    time.sleep(random.uniform(0.03, 0.04))
    controller.tap('a')
    time.sleep(random.uniform(0.03, 0.04))
    controller.release(Key.shift_l)
    time.sleep(random.uniform(0.03, 0.04))
    controller.tap(Key.home)
    time.sleep(random.uniform(0.03, 0.04))
    controller.tap(Key.enter)