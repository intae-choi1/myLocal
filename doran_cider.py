from pynput.keyboard import Key, Controller as kc, Listener as kl
from multiprocessing import Process, Value, Array
import pyautogui as pag
import time, random, os
from datetime import datetime


def press_and_release(key, delay=0.25):
    kc.press(key)
    time.sleep(delay)
    kc.release(key)
    
def mouse_click(x, y, wait=0.2):
    pag.click(x, y)
    time.sleep(wait)

def on_release(key):
    compare = key.char if hasattr(key, "char") else key.name
    if compare == 'f10': # 시작
        run_flag.value = True
    elif compare == 'f11': # 일시중지
        run_flag.value = False
        print(run_flag.value)
        try:
            my_process.terminate()
        except NameError:
            pass
    elif compare == 'f12' or compare == 'esc': # 종료
        run_flag.value = False
        alive_flag.value = False
        try:
            my_process.terminate()
        except NameError:
            pass
        return False
    elif compare == 'p':
        print(pag.position())
        
def target_process(run_flag):
    pag.FAILSAFE = False
    for i in range(10):        
        if i == 0:
            pag.click(*pag.position(), 2, 0.1)
        else:
            pag.click(*pag.position(), 1, 0.1)
        time.sleep(0.35)
        pag.press("enter")
        time.sleep(0.2)

if __name__ == "__main__":
    run_flag = Value('i', False)
    alive_flag = Value('i', True)
    
    listener = kl(
        on_release=on_release
    )
    listener.start()
    
    while alive_flag.value:
        if run_flag.value:
            print(f'시작 {datetime.now().strftime("%H:%M:%S")}')
            my_process = Process(target=target_process, args=(run_flag,))
            my_process.start()
            my_process.join()
            break
        else:
            # print("시작 대기중")
            time.sleep(1)