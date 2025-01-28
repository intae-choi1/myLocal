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
def king_click(stop_event, lock, controller, stores, combis, physics, key, x):
    y=85
    while not stop_event.is_set():
        sleep(stop_event, 0.1)
        for _ in range(2):
            # 왕퀘 취소, 수락
            mouse_click(stop_event, x, y)                           # 왕클릭
            press_and_release(stop_event, controller, Key.enter, 0.35)
            press_and_release(stop_event, controller, Key.enter, 0.3)
            press_and_release(stop_event, controller, Key.down, 0.2)
            press_and_release(stop_event, controller, Key.enter, 0.3)
            press_and_release(stop_event, controller, Key.enter, 0.2)
            press_and_release(stop_event, controller, Key.enter, 0.2)
            press_and_release(stop_event, controller, Key.esc, 0.2)
            press_and_release(stop_event, controller, 's', 0.2)
            press_and_release(stop_event, controller, Key.page_down, 0.2)
            press_and_release(stop_event, controller, Key.page_down, 0.05)
            
            sleep(stop_event, 0.8)


########################## 스킬 ##########################
####### 단일 키 #######
# 탭탭
def tabtab(event, lock, controller, stores, combis, physics, key):
    time.sleep(0.02)
    controller.tap(Key.tab)
    time.sleep(0.085)
    controller.tap(Key.tab)
    time.sleep(0.03)
    for i in range(5):
        controller.tap('4')
        time.sleep(0.08)


# 혼 5번
def skill_curse(event, lock, controller, stores, combis, physics, key, char):
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


# 무빙혼
def moving_curse(event, lock, controller, stores, combis, physics, key):
    if not lock.locked():
        lock.acquire()
        controller.tap(Key.esc)
        # time.sleep(0.05)
        controller.tap(physics['direction'])
        time.sleep(0.05)
        controller.tap('3')
        time.sleep(0.05)
        controller.tap(physics['direction'])
        time.sleep(0.05)
        controller.tap(Key.enter)
        lock.release()


####### 조합 키 #######
# shift로 쓰는 skill 5번
def skill_roll(event, lock, controller, stores, combis, physics, key, char):
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


# 부활
def revive(event, lock, controller, stores, combis, physics, key):
    time.sleep(random.uniform(0.03, 0.04))
    controller.tap(Key.esc)
    time.sleep(random.uniform(0.03, 0.04))
    controller.press(Key.shift)
    time.sleep(random.uniform(0.03, 0.04))
    controller.tap('z')
    time.sleep(random.uniform(0.03, 0.04))
    controller.tap('a')
    time.sleep(random.uniform(0.03, 0.04))
    controller.release(Key.shift_l)
    time.sleep(random.uniform(0.03, 0.04))
    controller.tap(Key.home)
    time.sleep(random.uniform(0.03, 0.04))
    controller.tap(Key.enter)


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


# 비영사천문
def skill_biyoung(event, lock, controller, stores, combis, physics, key):
    controller.press(Key.shift_l)
    time.sleep(0.015)
    controller.tap('z')
    controller.release(Key.shift_l)
    time.sleep(0.015)
    controller.tap('n')


####### 키 누를 때 #######
# 무빙힐 자동
def moving_heal(event, lock, controller, stores, combis, physics, key):
    if not lock.locked():
        lock.acquire()
        for _ in range(5):
            controller.tap('4')
            time.sleep(0.02)
            controller.tap(physics['direction'])
            time.sleep(0.02)
        lock.release()