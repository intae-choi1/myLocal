import time
import pyautogui as pag
from datetime import datetime
from pynput import keyboard
from pynput.mouse import Button, Controller as MC
from pynput.keyboard import Key, Controller as KC
import random

class MyExcetion(Exception):
    def __init__(self,msg):
        self.msg=msg
    def __str__(self):
        return self.msg
    
class MyExcetion2(Exception):
    def __init__(self,msg):
        self.msg=msg
    def __str__(self):
        return self.msg
    
def k_on_press(key):
    pass

def k_on_release(key):
    compare = key.char if hasattr(key, 'char') else key.name
    # print(compare, key)
    if compare == "esc":
        return False # Stop listener
    elif compare == "p":
        print(mc.position)
  
    
def k_press_and_release(key, duration=0.05):
    time.sleep(0.02)
    kc.press(key)
    time.sleep(duration)
    kc.release(key)
    time.sleep(0.02)


def m_move_and_click(x, y, times=1):
    mc.position = x, y
    mc.click(Button.left, times)
    time.sleep(0.25)
    
    
def main():
    listener = keyboard.Listener(
        on_press=k_on_press,
        on_release=k_on_release
    )
    # listener.start()
    
    m_move_and_click(850, 120, 1)
    for _ in range(17):
        m_move_and_click(800, 450, 1) # charli클릭
        m_move_and_click(1800, 800, 1) # 다음
        m_move_and_click(1720, 935, 1) # 예
        m_move_and_click(1630, 700, 1) # 빈공간
        #휠
        for _ in range(50):
            mc.scroll(0,-10)
            time.sleep(0.01)
        time.sleep(0.2)
        m_move_and_click(1130, 510, 1) # 좀비
        m_move_and_click(1720, 935, 1) # 예
        m_move_and_click(1800, 800, 1)  # 다음
        
    # listener.join()

if __name__ == "__main__":
    mc = MC()
    kc = KC()
    
    main()
