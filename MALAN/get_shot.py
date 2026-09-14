import os, time
from datetime import datetime
import mss
import keyboard, pyautogui
import numpy as np
import cv2 

# 캡처할 영역
# left, top, width, height
REGION = (300, 35, 50, 25)

# 저장 폴더
SAVE_DIR = "../imgs/mooreung/floor"
os.makedirs(SAVE_DIR, exist_ok=True)


def take_screenshot():
    left, top, width, height = REGION
    monitor = {"left": left, "top": top, "width": width, "height": height}

    with mss.MSS() as sct:
        screenshot = sct.grab(monitor)
        scr = np.array(screenshot)
        img = cv2.cvtColor(scr, cv2.COLOR_BGRA2RGB)
        print(img)
        img = cv2.cvtColor(scr, cv2.COLOR_BGRA2GRAY)
        print(img)

    filename = datetime.now().strftime("screenshot_%Y%m%d_%H%M%S.png")
    filepath = os.path.join(SAVE_DIR, filename)

    mss.tools.to_png(screenshot.rgb, screenshot.size, output=filepath)

    print(f"저장 완료: {filepath}")


print("F8 키를 누르면 지정 영역을 캡처합니다.")
print("ESC 키를 누르면 종료합니다.")

keyboard.add_hotkey("f8", take_screenshot)

keyboard.wait("esc")

