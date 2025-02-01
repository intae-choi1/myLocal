import time, random

import pyautogui as pag
from pynput.keyboard import Key


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
    controller.press(key)
    controller.release(key)
    time.sleep(delay)


########################## 마우스 동작 ##########################
def king_click(stop_event, lock, controller, stores, combis, physics, key):
    x,y = 685, 225 # 오른쪽에서
    x,y = 1315, 230 # 왼쪽에서
    x,y = 1130, 240 # 왼쪽에서
    while not stop_event.is_set():
        sleep(stop_event, 0.1)
        for _ in range(10):
            mouse_click(stop_event, x, y, 0.05)
        press_and_release(stop_event, controller, 's', 0.2)
        press_and_release(stop_event, controller, Key.page_down, 0.2)
        press_and_release(stop_event, controller, Key.page_down, 0.1)
        press_and_release(stop_event, controller, Key.page_down, 0.01)
        sleep(stop_event, 0.7)


########################## 스킬 ##########################
######################### 단일 키 #########################
# 탭탭
def tabtab(event, lock, controller, stores, combis, physics, key):
    time.sleep(0.02)
    controller.tap(Key.tab)
    time.sleep(0.08)
    controller.tap(Key.tab)
    time.sleep(0.02)
    for i in range(5):
        controller.tap('4')
        time.sleep(0.08)


# skill 5번
def skill_roll(event, lock, controller, stores, combis, physics, key, char):
    if not lock.locked():
        lock.acquire()

        n = 0.5
        rand = random.uniform(0.085, 0.09)
        delay1 = rand * n
        delay2 = rand * n * 0.8
        time.sleep(delay2)
        controller.tap(Key.esc)
        for i in range(5):
            time.sleep(delay1)
            controller.tap(char)
            time.sleep(delay2)
            controller.tap(physics['direction'])
            time.sleep(delay2)
            controller.tap(Key.enter)

        lock.release()


# 무빙 스킬
def moving_skill(event, lock, controller, stores, combis, physics, key, char):
    if not lock.locked():
        lock.acquire()

        controller.tap(Key.esc)
        time.sleep(0.02)
        controller.tap(physics['direction'])
        time.sleep(0.05)
        controller.tap(char)
        time.sleep(0.05)
        controller.tap(physics['direction'])
        time.sleep(0.05)
        controller.tap(Key.enter)

        lock.release()


######################### 조합 키 #########################
# skill 5번 (shift로 사용)
def skill_roll_shift(event, lock, controller, stores, combis, physics, key, char):
    if not lock.locked():
        lock.acquire()
        n = 0.25
        for i in range(5):
            time.sleep(random.uniform(0.085, 0.09)*n)
            controller.press(Key.shift)
            time.sleep(random.uniform(0.085, 0.09)*n)
            controller.tap('z')
            time.sleep(random.uniform(0.085, 0.09)*n)
            controller.tap(char)
            time.sleep(random.uniform(0.085, 0.09)*n)
            controller.release(Key.shift_l)
            time.sleep(random.uniform(0.085, 0.09)*n)
            controller.tap(Key.right)
            time.sleep(random.uniform(0.085, 0.09)*n)
            controller.tap(Key.enter)
        lock.release()


# 물약 3번 빨기 (ctrl+e * 3)
def drink(event, lock, controller, stores, combis, physics, key):
    n = 0.2
    for i in range(3):
        time.sleep(random.uniform(0.04, 0.05))
        controller.press(Key.ctrl_l)
        time.sleep(random.uniform(0.085, 0.09)*n)
        controller.tap('e')
        time.sleep(random.uniform(0.085, 0.09)*n)
        controller.release(Key.ctrl_l)
    physics['e'] = True


######################### 키 누를 때 #########################
# 무빙힐 자동
def moving_heal(event, lock, controller, stores, combis, physics, key):
    if not lock.locked():
        lock.acquire()
        controller.tap(physics['direction'])
        for _ in range(5):
            time.sleep(0.02)
            controller.tap('4')
        lock.release()