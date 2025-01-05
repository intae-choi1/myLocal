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

        
    m_move_and_click(1200, 120, 1, is_notebook)

    
    for _ in range(25):
        m_move_and_click(1473, 915, 1, is_notebook) # 가가
        m_move_and_click(1383, 876, 1, is_notebook) # 달꽃
        m_move_and_click(1639, 902, 1, is_notebook) # 다음
        m_move_and_click(1707, 801, 1, is_notebook) # 다음

        
    # listener.join()

if __name__ == "__main__":
    mc = Mc()
    kc = Kc()
    
    main()
