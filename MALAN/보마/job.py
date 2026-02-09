import time, random

import pyautogui as pag
from pynput.keyboard import Key

from 공통.utils import deco1
from 공통.job import press_and_release

######################### 조합 키 #########################
# 쉬프트 꾹 누르기
@deco1
def use_shift(event, lock, controller, stores, combis, physics, key):
    if physics['shift_toggle']:
        controller.press(Key.shift_l)
    else:
        controller.release(Key.shift_l)
    physics['shift_toggle'] = not physics['shift_toggle']

# 점프와 스킬샷 동시에
@deco1
def jump_skill(event, lock, controller, stores, combis, physics, key, char):
    controller.tap(char)
    controller.tap(Key.space)