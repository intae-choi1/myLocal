import time, random

import pyautogui as pag
from pynput.keyboard import Key


######################### 조합 키 #########################
# temp
def to_king(event, lock, controller, stores, combis, physics, key):
    time.sleep(random.uniform(0.04, 0.05))
    controller.tap('0')
    time.sleep(random.uniform(0.04, 0.05))
    controller.tap('4')
    time.sleep(random.uniform(0.04, 0.05))
    controller.tap(Key.enter)
    time.sleep(random.uniform(0.1, 0.2))
    controller.tap('9')
    time.sleep(random.uniform(0.1, 0.2))
    controller.type('오월랑')
    time.sleep(random.uniform(0.03, 0.04))
    controller.tap(Key.enter)


