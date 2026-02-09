import time, random

import pyautogui as pag
from pynput.keyboard import Key

from 공통.utils import deco1, sleep
from 공통.job import press_and_release

######################### 조합 키 #########################
# 쉬프트 꾹 누르기
@deco1
def use_shift(event, lock, controller, stores, combis, physics, key):
    while not event.is_set():
        controller.press(Key.shift_l)
        sleep(event, 0.01)
        controller.release(Key.shift_l)
        sleep(event, 0.02)