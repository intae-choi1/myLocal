import time, random

import pyautogui as pag
from pynput.keyboard import Key

from 공통.deco import deco1
from 공통.job import sleep, press_and_release

######################### 조합 키 #########################
@deco1
def to_king(event, lock, controller, stores, combis, physics, key, character_name):
    sleep(event, random.uniform(0.04, 0.05))
    press_and_release(event, controller, '0', random.uniform(0.04, 0.05))
    press_and_release(event, controller, '4', random.uniform(0.04, 0.05))
    press_and_release(event, controller, Key.enter, random.uniform(0.1, 0.2))
    press_and_release(event, controller, '9', random.uniform(0.1, 0.2))
    controller.type(character_name)
    time.sleep(random.uniform(0.03, 0.04))
    press_and_release(event, controller, Key.enter, random.uniform(0.4, 0.5))
    press_and_release(event, controller, Key.left, random.uniform(0.1, 0.1))
    controller.press(Key.up)


@deco1
def to_hyung(event, lock, controller, stores, combis, physics, key, character_name):
    time.sleep(random.uniform(0.04, 0.05))
    controller.press(Key.ctrl_l)
    time.sleep(random.uniform(0.04, 0.05))
    press_and_release(event, controller, 'q', random.uniform(0.04, 0.05))
    controller.release(Key.ctrl_l)
    time.sleep(random.uniform(0.1, 0.2))
    press_and_release(event, controller, '9', random.uniform(0.1, 0.2))
    controller.type(character_name)
    time.sleep(random.uniform(0.03, 0.04))
    press_and_release(event, controller, Key.enter, random.uniform(0.4, 0.5))
    controller.tap(Key.up)


@deco1
def bomu(event, lock, controller, stores, combis, physics, key):
    delay = 0.02
    for char in ['r', 's']:
        controller.press(Key.shift_l)
        time.sleep(delay)
        controller.tap('z')
        controller.release(Key.shift_l)
        time.sleep(delay)
        press_and_release(event, controller, char, 0.08)
        press_and_release(event, controller, Key.home, delay)
        press_and_release(event, controller, Key.enter, delay)