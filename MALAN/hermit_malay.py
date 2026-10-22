import time
import cv2
import pyautogui
import mss
import requests
import numpy as np
from functools import reduce
from enum import IntEnum, auto

discord_url = "https://discord.com/api/webhooks/1542561015991115827/Vxq4bf2E9XcNunptL2XEiEJmN79ZLapeRRnOtRZyK0CaQGEzCHwbRkGX0YJuJXmyAuxp"
pyautogui.PAUSE=.01

# 랩탑 설정
# monitor = {"left":0, "top":0, "width":1920, "height":1080}
# mp_slash_rois = [(421+i*6, 1003, 7, 7) for i in range(4)]
# mp_n_rois = [(415+i*6, 1003, 5, 7) for i in range(4)]
# hp_slash_rois = [(309+i*6, 1003, 7, 7) for i in range(4)]
# hp_n_rois = [(303+i*6, 1003, 5, 7) for i in range(4)]
# slash_template = cv2.imread("../imgs/templates/mp_slash.png", cv2.IMREAD_COLOR)
# mphp_templates = [cv2.imread(f"../imgs/templates/mp_{i}.png", cv2.IMREAD_COLOR) for i in range(10)]


# 데스크탑 설정
monitor = {"left":0, "top":0, "width":2560, "height":1440}
mp_slash_rois = [(796+i*12, 1323, 14, 14) for i in range(4)]
mp_n_rois = [(784+i*12, 1323, 10, 14) for i in range(4)]
hp_slash_rois = [(572+i*12, 1323, 14, 14) for i in range(4)]
hp_n_rois = [(560+i*12, 1323, 10, 14) for i in range(4)]
slash_template = cv2.imread("../imgs/templates/mp_slash.png", cv2.IMREAD_COLOR)
mphp_templates = [cv2.imread(f"../imgs/templates/mp_{i}.png", cv2.IMREAD_COLOR) for i in range(10)]

mphp_threshold = 0.9


# 화면
def get_screenshot(sct):
    img = np.array(sct.grab(monitor))
    return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

def crop(img, roi):
    x, y, w, h = roi
    return img[y:y+h, x:x+w]

def match(img, template, threshold=0.7, roi=None):
    if roi:
        base = crop(img, roi)
    else:
        base = img

    result = cv2.matchTemplate(base, template, cv2.TM_CCOEFF_NORMED)
    _, score, _, pos = cv2.minMaxLoc(result)

    if score < threshold:
        return (None, None, score)

    if roi:
        pos=(pos[0]+roi[0], pos[1]+roi[1])
    h, w, c = template.shape

    return (pos[0]+w//2, pos[1]+h//2, score)


def get_stat(screenshot, slash_rois, number_rois):
    # 현재 몇 자리인지 '/' 위치로 판단
    digit_count = 0
    for i, roi in enumerate(slash_rois):
        score = match(screenshot, slash_template, mphp_threshold, roi=roi)[2]
        if score > mphp_threshold:
            digit_count = i + 1
            break

    if digit_count == 0:
        return -1

    # 각 자리의 숫자 인식
    digits = []

    for roi in number_rois[:digit_count]:   
        scores = [
            match(screenshot, template, mphp_threshold, roi=roi)[2] 
            for template in mphp_templates
        ]
        digits.append(np.argmax(scores))

    return int(reduce(lambda x,y: x*10+y, digits))

def get_mp(screenshot):
    return get_stat(screenshot, mp_slash_rois, mp_n_rois)

def get_hp(screenshot):
    return get_stat(screenshot, hp_slash_rois, hp_n_rois)


class State(IntEnum):
    INIT = auto()
    CHARGE_MP = auto()
    CHARGE_HP = auto()

class Runner:
    def __init__(self):
        self.state = State.INIT
        self.substate = None
        self.keys = set()               # 눌린 키 모음 세트


        self.acting = False             # 액션이 진행중인지 확인용
        self.action_start = 0           # 액션 시간 기록용


    def press(self, key):
        self.keys.add(key)
        pyautogui.keyDown(key)

    def release(self, key):
        if key in self.keys:
            self.keys.remove(key)
        pyautogui.keyUp(key)

    def release_all(self):
        for key in self.keys:
            pyautogui.keyUp(key)
        self.keys.clear()

    def start_action(self):
        self.action_start = time.monotonic()
        self.acting = True

    def action_done(self, duration=0):
        if not self.acting:
            return False
        if time.monotonic() >= self.action_start + duration:
            self.acting = False
            return True
        return False


    def update(self, screenshot):
        mp = get_mp(screenshot)
        hp = get_hp(screenshot)

        if mp == -1 or hp == -1:
            print(f"{mp=} {hp=} 인식 불가")
            return


        if self.state < State.CHARGE_HP and hp < 1800:
            print(f"{hp=} 1800 미만")
            self.action_done()
            self.state = State.CHARGE_HP
            return

        if self.state < State.CHARGE_MP and mp < 200:
            print(f"{mp=} 200 미만")
            self.action_done()
            self.state = State.CHARGE_MP
            return


        if self.state == State.CHARGE_HP:
            if not self.acting:
                self.press("delete")
                self.start_action()
                self.substate = "WAIT"
            elif self.substate == "WAIT" and self.action_done(0.2):
                self.release("delete")
                self.substate = None
                self.state = State.INIT
            return

        if self.state == State.CHARGE_MP:
            if not self.acting:
                self.press("ctrl")
                self.start_action()
                self.substate = "WAIT"
            elif self.substate == "WAIT" and self.action_done(0.2):
                self.release("ctrl")
                self.substate = None
                self.state = State.INIT
            return


def main():
    runner = Runner()
    print("1초 후 시작합니다.")
    time.sleep(1)
    try:
        with mss.MSS() as sct:
            while True:
                screenshot = get_screenshot(sct)
                runner.update(screenshot)
                time.sleep(0.01)

    except Exception as e:
        raise e
    
    finally:
        runner.release_all()



if __name__ == "__main__":
    main()
