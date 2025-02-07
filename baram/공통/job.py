import time, random

import pyautogui as pag
from pynput.keyboard import Key

from .deco import deco1


def sleep(stop_event, t):
    if stop_event.is_set():
        return
    time.sleep(t)
    

def mouse_click(stop_event, x, y, wait=0.15):
    if stop_event.is_set():
        return
    pag.click(x, y)
    time.sleep(wait)


def press_and_release(stop_event, controller, key, delay=0.25):
    if stop_event.is_set():
        return
    controller.tap(key)
    time.sleep(delay)


########################## 마우스 동작 ##########################
@deco1
def king_click(stop_event, lock, controller, stores, combis, physics, key):
    x,y = 705, 155 # 오른쪽에서
    # x,y = 765, 80 # 오른쪽에서
    # x,y = 1315, 230 # 왼쪽에서
    # x,y = 1130, 240 # 왼쪽에서
    while not stop_event.is_set():
        for _ in range(12):
            mouse_click(stop_event, x, y, 0.025)
        press_and_release(stop_event, controller, 's', 0.1)
        for _ in range(5):
            press_and_release(stop_event, controller, Key.page_down, 0.1)
        # for mob in ["mongdal", "bug"]:
        for mob in ["ghost", "bug"]:
            try:
                pag.locateCenterOnScreen(f"imgs/{mob}.png", region=(1800, 210, 200, 140), confidence=0.8)
                print("흉퀘 나옴")
                stop_event.set()
                break
            except pag.ImageNotFoundException:
                sleep(stop_event, 0.15 if mob == "bug" else 0)


########################## 스킬 ##########################
######################### 단일 키 #########################
# 탭탭
@deco1
def tabtab(event, lock, controller, stores, combis, physics, key):
    press_and_release(event, controller, Key.tab, 0.08)
    press_and_release(event, controller, Key.tab, 0.02)
    for i in range(5):
        controller.tap('4')
        time.sleep(0.02)


# 무빙 스킬
@deco1
def moving_skill(event, lock, controller, stores, combis, physics, key, char):
    press_and_release(event, controller, Key.esc, 0.02)
    press_and_release(event, controller, physics['direction'], 0.04)
    press_and_release(event, controller, char, 0.04)
    press_and_release(event, controller, physics['direction'], 0.04)
    press_and_release(event, controller, Key.enter, 0.04)


# skill 5번
@deco1
def skill_roll(event, lock, controller, stores, combis, physics, key, char):
    delay1 = 0.035
    delay2 = delay1 * 0.8
    controller.tap(Key.esc)
    time.sleep(delay1)
    for i in range(5):
        press_and_release(event, controller, char, delay1)
        press_and_release(event, controller, physics['direction'], delay2)
        press_and_release(event, controller, Key.enter, delay1)


######################### 조합 키 #########################
# skill 5번 (shift로 사용)
@deco1
def skill_roll_shift(event, lock, controller, stores, combis, physics, key, char):
    n = 0.25
    time.sleep(0.02)
    for i in range(5):
        controller.press(Key.shift_l)
        time.sleep(0.03)
        press_and_release(event, controller, 'z', 0.02)
        press_and_release(event, controller, char, 0.02)
        controller.release(Key.shift_l)
        time.sleep(0.02)
        press_and_release(event, controller, physics['direction'], 0.03)
        press_and_release(event, controller, Key.enter, 0.02)


# 물약 3번 빨기 (ctrl+e * 3)
@deco1
def drink(event, lock, controller, stores, combis, physics, key):
    n = 0.2
    for i in range(3):
        controller.press(Key.ctrl_l)
        time.sleep(random.uniform(0.085, 0.09)*n)
        press_and_release(event, controller, 'e', random.uniform(0.085, 0.09)*n)
        controller.release(Key.ctrl_l)
        time.sleep(random.uniform(0.04, 0.05))
    physics['e'] = True


######################### 키 누를 때 #########################
# 무빙힐 자동
@deco1
def moving_heal(event, lock, controller, stores, combis, physics, key):
    controller.tap(physics['direction'])
    for _ in range(5):
        press_and_release(event, controller, '4', 0.02)





