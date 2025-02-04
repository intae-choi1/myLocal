import time, random

import pyautogui as pag
from pynput.keyboard import Key

from 공통.deco import deco1


######################### 조합 키 #########################
@deco1
def to_king(event, lock, controller, stores, combis, physics, key, character_name):
    time.sleep(random.uniform(0.04, 0.05))
    controller.tap('0')
    time.sleep(random.uniform(0.04, 0.05))
    controller.tap('4')
    time.sleep(random.uniform(0.04, 0.05))
    controller.tap(Key.enter)
    time.sleep(random.uniform(0.1, 0.2))
    controller.tap('9')
    time.sleep(random.uniform(0.1, 0.2))
    controller.type(character_name)
    time.sleep(random.uniform(0.03, 0.04))
    controller.tap(Key.enter)
    time.sleep(random.uniform(0.4, 0.5))
    controller.tap(Key.left)


@deco1
def to_hyung(event, lock, controller, stores, combis, physics, key, character_name):
    time.sleep(random.uniform(0.04, 0.05))
    controller.press(Key.ctrl_l)
    time.sleep(random.uniform(0.04, 0.05))
    controller.tap('q')
    time.sleep(random.uniform(0.04, 0.05))
    controller.release(Key.ctrl_l)
    time.sleep(random.uniform(0.1, 0.2))
    controller.tap('9')
    time.sleep(random.uniform(0.1, 0.2))
    controller.type(character_name)
    time.sleep(random.uniform(0.03, 0.04))
    controller.tap(Key.enter)
    time.sleep(random.uniform(0.4, 0.5))
    controller.tap(Key.up)