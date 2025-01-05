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
    for _ in range(2):
        x, y = pag.locateCenterOnScreen("imgs/jane.png", region=(550, 600, 1300, 1200), confidence=0.85)
        y -= 50
        m_move_and_click(x, y, 2) # jane클릭
        m_move_and_click(1700, 800, 1) # 다음
        m_move_and_click(1650, 700, 1) # 빈공간
        m_move_and_click(1150, 715, 1) # 장어 ##########
        m_move_and_click(1150, 745, 1) # 입력창
        for i in ["1", "0", "0"]:
            k_press_and_release(i)
            
        m_move_and_click(1730, 910, 1) # 확인
        m_move_and_click(1650, 910, 1) # 예
        m_move_and_click(830, 910, 1) # 대화 종료
        
    # listener.join()

if __name__ == "__main__":
    mc = MC()
    kc = KC()
    
    main()
