import time
import pyautogui as pag
from pynput.keyboard import (
    Key, 
    KeyCode,
)


# 메이플월드일때만 실행 
# lock되지 않았을때만 ← 2번째 인자가 lock객체인 함수에만 적용
# lock걸고 시작, 끝나면 lock 해제
def deco1(func):
    def wrapper(*args, **kwargs):
        # s = time.time()
        w = pag.getActiveWindow()
        if (w and w.title.startswith("Maple")):
            lock = args[1]
            if not lock.locked():
                lock.acquire()
                func(*args, **kwargs)
                lock.release()
        # e = time.time()
        # print(f"{func.__name__} {e-s:.5f} seconds elapsed.")
    return wrapper


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


# 키 누를때, 키조합 인식을 위해 set에 키 추가
def add_combi(stores, physics, key):
    if key == Key.ctrl_l:
        stores['ctrl'].add(key)
    
    elif isinstance(key, KeyCode) and key.vk == 50:
        stores['2'].add(KeyCode(char='2'))
        
    elif isinstance(key, KeyCode) and key.vk == 51:
        stores['3'].add(KeyCode(char='3'))
        
    elif isinstance(key, KeyCode) and key.vk == 52:
        stores['4'].add(KeyCode(char='4'))
    
    elif isinstance(key, KeyCode) and key.vk == 53:
        stores['5'].add(KeyCode(char='5'))
        
    elif isinstance(key, KeyCode) and key.vk == 69:
        if physics['e']:
            stores['e'].add(KeyCode(char='e'))


# 키 뗄때, set에서 키 삭제
def remove_combi(stores, physics, key):
    if key == Key.ctrl_l:
        if key in stores['ctrl']:
            stores['ctrl'].remove(key)
    
    elif isinstance(key, KeyCode) and key.vk == 50:
        c = '2'
        key_ = KeyCode(char=c)
        if key_ in stores[c]:
            stores[c].remove(key_)
            
    elif isinstance(key, KeyCode) and key.vk == 51:
        c = '3'
        key_ = KeyCode(char=c)
        if key_ in stores[c]:
            stores[c].remove(key_)
        
    elif isinstance(key, KeyCode) and key.vk ==52:
        c = '4'
        key_ = KeyCode(char=c)
        if key_ in stores[c]:
            stores[c].remove(key_)
    
    elif isinstance(key, KeyCode) and key.vk ==53:
        c = '5'
        key_ = KeyCode(char=c)
        if key_ in stores[c]:
            stores[c].remove(key_)
    
    elif isinstance(key, KeyCode) and key.vk == 69:
        c = 'e'
        key_ = KeyCode(char=c)
        if key_ in stores[c]:
            stores[c].remove(key_)