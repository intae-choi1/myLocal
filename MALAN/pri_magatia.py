import time
import cv2
import pyautogui
import numpy as np
from functools import reduce
from enum import IntEnum, auto
import mss


pyautogui.PAUSE=.01
TARGET_RGB = np.array([255, 255, 136])
TARGET_BGR = np.array([136, 255, 255])
TOLERANCE = 10
MIN_PIXELS = 1

monitor = {"left":0, "top":0, "width":2560, "height":1380}
minimap_roi = (170, 170, 160, 100)
mp_slash_rois = [(796+i*12, 1323, 14, 14) for i in range(4)]
mp_n_rois = [(784+i*12, 1323, 10, 14) for i in range(4)]
slash_template = cv2.imread("../imgs/mooreung/templates/mp_slash.png", cv2.IMREAD_COLOR)
mphp_templates = [cv2.imread(f"../imgs/mooreung/templates/mp_{i}.png", cv2.IMREAD_COLOR) for i in range(10)]

mphp_threshold = 0.99

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

    return reduce(lambda x,y: x*10+y, digits)

def get_mp(screenshot):
    return get_stat(screenshot, mp_slash_rois, mp_n_rois)

def get_player(screenshot):
    img = crop(screenshot, minimap_roi)
    # 색상 차이 계산
    diff = np.abs(img.astype(np.int16) - TARGET_BGR)
    # 모든 RGB 채널이 허용 범위 안에 있는지 검사
    mask = np.all(diff <= TOLERANCE, axis=2)
    # 노란색 픽셀 좌표
    y, x = np.where(mask)

    if len(x) < MIN_PIXELS:
        return None

    # 노란색 영역의 중심
    center_x, center_y = int(x.mean()), int(y.mean())
    # 화면 전체 기준 좌표
    screen_x, screen_y = minimap_roi[0] + center_x, minimap_roi[1] + center_y

    return screen_x, screen_y


class State(IntEnum):
    INIT = auto()
    ATTACK = auto()
    SYMBOL = auto()
    MOVING = auto()
    CHARGE_MP = auto()
    ATTACK2 = auto()

class Runner:
    def __init__(self):
        self.state = State.ATTACK
        self.substate = None
        self.keys = set()               # 눌린 키 모음 세트
        self.player = (250, 243)              # 플레이어 위치

        self.acting = False             # 액션이 진행중인지 확인용
        self.action_start = 0           # 액션 시간 기록용

        self.move_key = None
        self.buff_start = 0
        self.attack_start = time.monotonic()

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
        player_x, player_y = get_player(screenshot)

        if player_x is not None:
            self.player = (player_x, player_y)

        print(self.state.name)
        print(self.player)

        if self.state < State.CHARGE_MP and mp < 200:
            self.action_done()
            self.state = State.CHARGE_MP
            return

        if self.state < State.MOVING and (player_x <= 240 or player_x >= 260):
            self.action_done()
            self.state = State.MOVING
            return

        # if self.state < State.SYMBOL and time.monotonic() > self.buff_start + 51:
        if self.state < State.SYMBOL and time.monotonic() > self.buff_start + 51:
            self.action_done()
            self.state = State.SYMBOL
            self.buff_start = time.monotonic()
            return

        if self.state < State.ATTACK2 and time.monotonic() > self.attack_start + 40:
            self.action_done()
            self.state = State.ATTACK2
            return


        if self.state == State.CHARGE_MP:
            if not self.acting:
                self.press("ctrl")
                self.start_action()
                self.substate = "WAIT"
            elif self.substate == "WAIT" and self.action_done(1):
                self.release("ctrl")
                self.substate = None
                self.state = State.ATTACK
            return

        if self.state == State.ATTACK:
            if "shift" in self.keys:
                self.release("shift")
            self.press("shift")
            self.state = State.INIT
            return

        if self.state == State.MOVING:
            move_key = "right" if self.player[0] < 250 else "left"
            if not self.acting:
                self.move_key = move_key
                self.release_all()
                self.press(self.move_key)
                self.press("x")
                self.start_action()
                self.substate = "MOVNIG"
            elif self.substate == "MOVNIG":
                if self.action_done(3) or (self.player[0] > 240 and self.player[0] < 260):
                    self.release_all()
                    self.acting = False
                    self.substate = None
                    self.state = State.ATTACK
                elif self.move_key != move_key:
                    print("방향전환")
                    self.move_key = move_key
                    self.release_all()
                    self.press(self.move_key)
                    self.press("x")
                    self.start_action()
            return

        if self.state == State.SYMBOL:
            if not self.acting:
                self.release_all()
                self.press("3")
                self.start_action()
                self.substate = "WAIT"
            elif self.substate == "WAIT" and self.action_done(1):
                self.release("3")
                self.substate = None
                self.state = State.ATTACK
            return

        if self.state == State.ATTACK2:
            print(self.substate)
            if not self.acting:
                self.release_all()
                self.press("left")
                self.press("x")
                time.sleep(0.1)
                self.press("shift")
                self.start_action()
                self.substate = "GO_LEFT1"
                self.attack_start = time.monotonic()
            elif self.substate == "GO_LEFT1" and self.action_done(0.2):
                self.release_all()
                self.start_action()
                self.substate = "GO_LEFT2"
            elif self.substate == "GO_LEFT2" and self.action_done(0.4):
                self.press("left")
                self.press("x")
                time.sleep(0.1)
                self.press("shift")
                self.start_action()
                self.substate = "GO_LEFT1"
            elif self.substate in ("GO_LEFT1", "GO_LEFT2") and time.monotonic() > self.attack_start + 1.3:
                self.release_all()
                self.press("right")
                self.press("x")
                time.sleep(0.1)
                self.press("shift")
                self.start_action()
                self.substate = "GO_RIGHT1"

            elif self.substate == "GO_RIGHT1" and self.action_done(0.2):
                self.release_all()
                self.start_action()
                self.substate = "GO_RIGHT2"
            elif self.substate == "GO_RIGHT2" and self.action_done(0.4):
                self.press("right")
                self.press("x")
                time.sleep(0.1)
                self.press("shift")
                self.start_action()
                self.substate = "GO_LEFT1"
            elif self.substate in ("GO_RIGHT1", "GO_RIGHT2") and time.monotonic() > self.attack_start + 5.5:
                self.substate = None
                self.state = State.ATTACK
                self.attack_start = time.monotonic()
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

    except Exception as e:
        raise e
    
    finally:
        runner.release_all()



if __name__ == "__main__":
    main()
