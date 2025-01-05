import time
import pyautogui as pag
from datetime import datetime
from pynput import keyboard
from pynput.mouse import Button, Controller as Mc
from pynput.keyboard import Key, Controller as Kc
import random


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
    time.sleep(0.45)
    
    
def main():
    listener = keyboard.Listener(
        on_press=k_on_press,
        on_release=k_on_release
    )
    listener.start()
    
    is_notebook = True
    if is_notebook:
        top_x, top_y = 1525, 80
        npc = "imgs/jini_notebook.png"
        region = (400, 400, 1250, 800)
        
        buffi = (835, 470)
        zombie_tenni = (835, 530)
        spirit = (835, 680) # scroll down 3
        
        next_1 = (835, 565)
        yes_1 = (1255, 695)
        next_2 = (1325, 610)
    else:
        top_x, top_y = 700, 20
        npc = "imgs/jini.png"
        region = (400, 400, 1250, 800) # 수정해야함
        
    m_move_and_click(top_x, top_y, 1)
    x, y = pag.locateCenterOnScreen(npc, region=region, confidence=0.9)
    y -= 50
    n = 1
    
    for _ in range(n):
        m_move_and_click(x, y, 1) # 찰리
        m_move_and_click(*next_1, 1) # 다음
        # m_move_and_click(1625, 890, 1) # 예
        # for _ in range(20):
        #     mc.scroll(0,-1)
        # else:
        #     time.sleep(0.45)
        m_move_and_click(*buffi, 1) # 항목 (루나, 러스터, 좀비)
        m_move_and_click(*yes_1, 1) # 예
        m_move_and_click(*next_2, 1) # 다음
        
    listener.join()

if __name__ == "__main__":
    mc = Mc()
    kc = Kc()
    
    main()
