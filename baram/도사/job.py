import time, random

import pyautogui as pag
from pynput.keyboard import Key

from 공통.deco import deco1
from 공통.job import sleep, press_and_release

######################### 조합 키 #########################
# 부활
@deco1
def revive(event, lock, controller, stores, combis, physics, key):
    press_and_release(event, controller, Key.esc, 0.03)
    controller.press(Key.shift)
    time.sleep(random.uniform(0.03, 0.04))
    press_and_release(event, controller, 'z', 0.03)
    press_and_release(event, controller, 'a', 0.03)
    controller.release(Key.shift_l)
    time.sleep(random.uniform(0.03, 0.04))
    press_and_release(event, controller, Key.home, 0.03)
    press_and_release(event, controller, Key.enter, 0)