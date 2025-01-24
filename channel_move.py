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
    is_notebook = False
    is_vm = True
    # n번째 유저
    n_user = 1
    
    if is_notebook:
        n_differ = 50
        x, y = 1530, 300 + n_differ*(n_user-1)
        x2, y2 = x + 110, y + 75
        x3, y3 = x - 650, y + 315 - n_differ*(n_user-1)
        x4, y4 = x - 550, y + 330 - n_differ*(n_user-1)
        add_delay = 0.5

    elif not is_notebook and is_vm:
        n_differ = 50
        x, y = 1400, 200 + n_differ*(n_user-1)
        x2, y2 = x + 65, y + 70
        x3, y3 = x - 650, y + 285 - n_differ*(n_user-1)
        x4, y4 = x - 550, y + 300 - n_differ*(n_user-1)
        add_delay = 0.5

    else:
        n_differ = 80
        x, y = 2150, 330 + n_differ*(n_user-1)
        x2, y2 = x + 120, y + 110
        x3, y3 = x - 1050, y + 470 - n_differ*(n_user-1)
        x4, y4 = x - 900, y + 500 - n_differ*(n_user-1)
        add_delay = 0.5
        
    while run_flag.value:
        mouse_click(x, y)                           # 유저
        mouse_click(x2, y2)                         # 같이 플레이 하기
        mouse_click(x3, y3, 2.5 + add_delay)   # 네
        mouse_click(x4, y4, 3.0 + add_delay + 3)   # 돌아가기

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
        else:
            # print("시작 대기중")
            time.sleep(1)