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


def king_click(stop_event, controller, x):
    y=85    
    while not stop_event.is_set():
        sleep(stop_event, 0.1)
        # 왕퀘 취소
        mouse_click(stop_event, x, y)                           # 왕클릭
        press_and_release(stop_event, controller, Key.enter, 0.2)
        press_and_release(stop_event, controller, Key.enter, 0.22)
        press_and_release(stop_event, controller, Key.down, 0.1)
        press_and_release(stop_event, controller, Key.enter, 0.17)
        press_and_release(stop_event, controller, Key.enter, 0.18)
        press_and_release(stop_event, controller, Key.enter, 0.18)
        press_and_release(stop_event, controller, Key.esc, 0.1)
        press_and_release(stop_event, controller, 's', 0.1)
        press_and_release(stop_event, controller, Key.page_down, 0.14)
        press_and_release(stop_event, controller, Key.page_down, 0.05)
        
        sleep(stop_event, 1.1)

        # 왕퀘 수락
        mouse_click(stop_event, x, y)                           # 왕클릭
        press_and_release(stop_event, controller, Key.enter, 0.2)
        press_and_release(stop_event, controller, Key.enter, 0.22)
        press_and_release(stop_event, controller, Key.down, 0.1)
        press_and_release(stop_event, controller, Key.enter, 0.17)
        press_and_release(stop_event, controller, Key.enter, 0.18)
        press_and_release(stop_event, controller, Key.enter, 0.18)
        press_and_release(stop_event, controller, Key.esc, 0.1)
        press_and_release(stop_event, controller, 's', 0.1)
        press_and_release(stop_event, controller, Key.page_down, 0.14)
        press_and_release(stop_event, controller, Key.page_down, 0.05)
        
        sleep(stop_event, 1.0)

    print("job1 중지")


########################## 스킬 ##########################
# 4번 스킬 4번 (기원)
def skill_4(stop_event, controller):
    for _ in range(4):
        rnd = random.uniform(0.085, 0.09)
        press_and_release(stop_event, controller, '4', rnd)
    

# 혼 5번
def skill_curse(stop_event, controller, physics, char):
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


# shift로 쓰는 skill 5번
def skill_roll(stop_event, controller, char):
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
    

# 비영사천문
def skill_biyoung(controller):
    controller.press(Key.shift_l)
    time.sleep(0.015)
    controller.tap('z')
    controller.release(Key.shift_l)
    time.sleep(0.015)
    controller.tap('n')
    
    
# 무빙힐 자동
def moving_heal(event, lock, controller, physics):
    if not lock.locked():
        lock.acquire()
        for _ in range(2):
            controller.tap('4')
            time.sleep(0.1)
            controller.tap(physics['direction'])
            time.sleep(0.24)
        lock.release()


# 무빙혼
def moving_curse(event, lock, controller, physics):
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


# 탭탭
def tabtab(event, lock, controller, physics):
    time.sleep(0.02)
    controller.tap(Key.tab)
    time.sleep(0.08)
    controller.tap(Key.tab)
    for i in range(4):
        time.sleep(0.08)
        controller.tap('4')
        


# 물약 3번 빨기 (ctrl+e * 3)
def drink(event, controller, physics):
    n = 0.2
    for i in range(3):
        time.sleep(random.uniform(0.04, 0.05))
        controller.press(Key.ctrl_l)
        time.sleep(random.uniform(0.085, 0.09)*n)
        controller.tap('e')
        time.sleep(random.uniform(0.085, 0.09)*n)
        controller.release(Key.ctrl_l)
    physics['e'] = True