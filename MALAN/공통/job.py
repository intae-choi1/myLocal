import time, random

import pyautogui as pag
from pynput.keyboard import Key

from .utils import deco1, mouse_click, press_and_release


########################## 마우스 동작 ##########################
@deco1
def channel_change(stop_event, lock, controller, stores, combis, physics, key):
    while not stop_event.is_set():
        nx = 560 + 170 * 3       # ※※채널 x방향 n번째 ※※
        ny = 250 + 60 * 10  # ※※채널 y방향 n번째 ※※
        while not stop_event.is_set():
            rx = random.randrange(0, 80)
            ry = random.randrange(0, 11)
            mouse_click(stop_event, 1695+rx, 1330+ry, 0)  # 메뉴
            mouse_click(stop_event, 1695+rx, 975+ry, 0.06)   # 채널변경
            # mouse_click(stop_event, 1695+rx, 975+ry, 0.09)   # 채널변경
            # mouse_click(stop_event, 1768, 855, 0.01)   # 아래 스크롤
            mouse_click(stop_event, nx+rx, ny+ry, 0)    # ※※채널※※
            press_and_release(stop_event, controller, Key.enter, 0.01)
            press_and_release(stop_event, controller, Key.esc, 0.06) # esc

@deco1
def put_cider(stop_event, lock, controller, stores, combis, physics, key):
    pack_stand_x, pack_stand_y = pag.locateCenterOnScreen("../imgs/meso_post.png", confidence=0.7)
    for i in range(12):
        try:
            x, y = pag.locateCenterOnScreen("../imgs/cider.png", confidence=0.9, region=(880, 40, 1600, 1400))
            package_x = pack_stand_x + 25  + (i%6)*100
            package_y = pack_stand_y - 180 + (i//6)*100
            mouse_click(stop_event, x, y, 0.12)
            mouse_click(stop_event, package_x, package_y, 0.08)
        except pag.ImageNotFoundException as e:
            print(e)
            break


########################## 스킬 ##########################
######################### 단일 키 #########################
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
    time.sleep(delay2)
    for i in range(5):
        press_and_release(event, controller, char, delay2)
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
    for i in range(3):
        controller.press(Key.ctrl_l)
        time.sleep(0.02)
        press_and_release(event, controller, 'e', 0.01)
        controller.release(Key.ctrl_l)
        time.sleep(0.04)
    physics['e'] = True


######################### 키 누를 때 #########################
# 무빙힐 자동
@deco1
def moving_heal(event, lock, controller, stores, combis, physics, key):
    controller.tap(physics['direction'])
    for _ in range(5):
        press_and_release(event, controller, '4', 0.02)





