from pynput.keyboard import Key, Controller as kc, Listener as kl
from pynput.mouse import Button, Controller as mc
import pyautogui as pg
import time, random, os


def on_press(key):
    pass

def on_release(key):
    compare = key.char if hasattr(key, "char") else key.name
    if compare == "esc": # 시작
        return False
    elif compare == "p":
        print(mc.position)
def main():
    listener = kl(
        on_press=on_press, on_release=on_release
    )
    listener.start()
    
    listener.join()
if __name__ == '__main__':
    mc = mc()
    kc = kc()
    main()