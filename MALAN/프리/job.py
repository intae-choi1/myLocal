import time, random

import pyautogui as pag
from pynput.keyboard import Key

from 공통.utils import deco1, sleep, mouse_click, press_and_release

######################### 조합 키 #########################
# 쉬프트 꾹 누르기
@deco1
def use_shift(event, lock, controller, stores, combis, physics, key):
    if physics['shift_toggle']:
        controller.press(Key.shift_l)
    else:
        controller.release(Key.shift_l)
    physics['shift_toggle'] = not physics['shift_toggle']

    # while not event.is_set():
    #     press_and_release(event, controller, "c", 0.7)
    #     sleep(event, 2)
    #     press_and_release(event, controller, Key.shift_l, 0.7)
    #     sleep(event, 2)

# 버프돌리기
@deco1
def buffs(event, lock, controller, stores, combis, physics, key):
    # press_and_release(event, controller, Key.end, 0.7)
    # press_and_release(event, controller, Key.delete, 1.5)
    # controller.press(Key.shift_l)
    # time.sleep(0.2)
    # controller.release(Key.shift_l)
    # # press_and_release(event, controller, Key.f5, 0.1)

    controller.press(Key.end)
    time.sleep(0.2)
    controller.release(Key.end)
    time.sleep(0.1)

    controller.press(Key.delete)
    time.sleep(1.1)
    controller.release(Key.delete)
    time.sleep(0.1)

    controller.press(Key.shift_l)
    time.sleep(0.8)
    controller.release(Key.shift_l)

# @deco1
def buffs2(event, lock, controller, stores, combis, physics, key):
    x, y = pag.locateCenterOnScreen("../imgs/cashop.png", confidence=0.7, region=(0, 800, 1920, 280))
    
    mouse_click(event, x, y-110, 0.2)

    controller.press(Key.end)
    time.sleep(0.2)
    controller.release(Key.end)
    time.sleep(0.1)

    controller.press(Key.delete)
    time.sleep(0.5)
    controller.release(Key.delete)

    controller.tap(Key.enter)
    time.sleep(0.2)
    controller.type("/파티탈퇴")
    time.sleep(0.2)
    controller.tap(Key.enter)
