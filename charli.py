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


def m_move_and_click(x, y, times=1, is_notebook=True):
    mc.position = x, y
    mc.click(Button.left, times)
    
    notebook_delay = 0.5 if is_notebook else 0
    time.sleep(0.45+notebook_delay)
    
    
def main():
    listener = keyboard.Listener(
        on_press=k_on_press,
        on_release=k_on_release
    )
    listener.start()
    
    is_notebook = False
    if is_notebook:
        top_x, top_y = 1525, 80
        npc = "imgs/charli_notebook.png"
        region = (500, 400, 1200, 800)
        
        luna = (835, 585)
        ruster = (835, 710)
        zombie = (835, 425) # scroll down 3
        
        next_1 = (1300, 600)
        yes_1 = (1250, 695)
        yes_2 = (1250, 695)
        next_2 = (1300, 610)
    else:
        top_x, top_y = 700, 20
        npc = "imgs/charli.png"
        region=(750, 650, 550, 350)
        
        luna = (1080, 750)
        ruster = (1075, 910)
        zombie = (1075, 535) # scroll down 3
        
        next_1 = (1700, 775)
        yes_1 = (1625, 890)
        yes_2 = (1630, 890)
        next_2 = (1700, 780)
        
    m_move_and_click(top_x, top_y, 1, is_notebook)
    x, y = pag.locateCenterOnScreen(npc, region=region, confidence=0.9)
    y -= 50
    n = 8
    
    for _ in range(n):
        m_move_and_click(x, y, 1, is_notebook) # 찰리
        m_move_and_click(*next_1, 1, is_notebook) # 다음
        m_move_and_click(*yes_1, 1, is_notebook) # 예
        # time.sleep(2)
        # for _ in range(20):
        #     mc.scroll(0,-1)
        # else:
        #     time.sleep(0.45)
        m_move_and_click(*ruster, 1, is_notebook) # 항목 (luna, ruster, zombie)
        m_move_and_click(*yes_2, 1, is_notebook) # 예
        m_move_and_click(*next_2, 1, is_notebook) # 다음
        
    # listener.join()

if __name__ == "__main__":
    mc = Mc()
    kc = Kc()
    
    main()
