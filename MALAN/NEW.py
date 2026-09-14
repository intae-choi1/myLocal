import time
import cv2
import pyautogui
import numpy as np
from functools import reduce
from enum import IntEnum, auto
import mss


pyautogui.PAUSE=.01
MAX_FLOOR = 33

game = {"left":0, "top":0, "width":2560, "height":1380}
floor_roi = (300, 35, 50, 25)
clear_coordinate = (1450, 80)
mp_slash_rois = [(796+i*12, 1323, 14, 14) for i in range(4)]
mp_n_rois = [(784+i*12, 1323, 10, 14) for i in range(4)]
hp_slash_rois = [(572+i*12, 1323, 14, 14) for i in range(5)]
hp_n_rois = [(560+i*12, 1323, 10, 14) for i in range(5)]
player_template = cv2.imread("../imgs/mooreung/templates/player.png", cv2.IMREAD_GRAYSCALE)
monster_template = cv2.imread("../imgs/mooreung/templates/monster.png", cv2.IMREAD_GRAYSCALE)
slash_template = cv2.imread("../imgs/mooreung/templates/mp_slash.png", cv2.IMREAD_GRAYSCALE)
mphp_templates = [cv2.imread(f"../imgs/mooreung/templates/mp_{i}.png", cv2.IMREAD_GRAYSCALE) for i in range(10)]
floor_templates = [cv2.imread(f"../imgs/mooreung/floor/{i}.png", cv2.IMREAD_GRAYSCALE) for i in range(-1, MAX_FLOOR+1)]

mphp_threshold = 0.99

# 화면
def get_screenshot(sct):
    img = np.array(sct.grab(game))
    return cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

def is_loading(screenshot):
    dark_ratio = np.mean(screenshot < 10)
    return dark_ratio > 0.9

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
    h, w = template.shape

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

def get_hp(screenshot):
    return get_stat(screenshot, hp_slash_rois, hp_n_rois)

def get_floor(screenshot):
    scores = [
        match(screenshot, template, roi=floor_roi)[2] 
        for template in floor_templates
    ]
    return np.argmax(scores)-1

def get_clear(screenshot):
    r = screenshot[clear_coordinate[1], clear_coordinate[0]]
    return True if r == 17 else False

def get_player(screenshot):
    x, y, s = match(screenshot, player_template, 0.7)
    if s < 0.7:
        return (None, None, s)
    return x+80, y, s

def get_monster(screenshot):
    x, y, s = match(screenshot, monster_template, 0.7)
    if s < 0.8:
        return (None, None, s)
    return x, y, s

class State(IntEnum):
    INIT = auto()
    GET_FLOOR = auto()
    FLOOR_ACTION = auto()
    FIND_MONSTER = auto()
    MOVE_TO_ATTACK = auto()
    ATTACK = auto()

    MOVE_TO_PORTAL1 = auto()
    UP_PORTAL1 = auto()
    MOVE_TO_PORTAL2 = auto()
    UP_PORTAL2 = auto()
    ESCAPE = auto()

class Runner:
    def __init__(self):
        self.state = State.INIT
        self.substate = None
        self.keys = set()               # 눌린 키 모음 세트
        self.floor = -2                 # 시작은 없는 층
        self.player = (700, 1200)              # 플레이어 위치
        self.monster = (1400, 1100)             # 몬스터 위치

        self.acting = False             # 액션이 진행중인지 확인용
        self.action_start = 0           # 액션 시간 기록용

        self.find_object_start = 0     # 몬스터 찾는 시간 기록용

        self.attack_start = 0           # 공격 시간 기록 용
        self.attack_timeout = 3         # 공격 최대 시간

        self.target_loc = None
        self.move_key = None
        self.face_key = None

    def reset_floor(self):
        self.player = (700, 1200)
        self.monster = (1400, 1100)
        self.find_object_start = 0
        self.attack_start = 0
        self.acting = False
        self.target_loc = None
        self.move_key = None
        self.face_key = None

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

    def check_priority(self, mp, hp):
        if self.state <= 5:
            if mp < 10 or hp < 1000:
                return State.ESCAPE

        return None

    def get_loc_dir(self):
        player_x = self.player[0]
        monster_x = self.monster[0]
        distance = abs(player_x - monster_x)
        # 둘 다 왼쪽에 몰림: 오른쪽으로 옮긴 뒤 왼쪽을 바라본다.
        if max(player_x, monster_x) < 600:
            target_loc = 1200
            move_key = "right"
            face_key = "left"
        # 둘 다 오른쪽에 몰림: 왼쪽으로 옮긴 뒤 오른쪽을 바라본다.
        elif min(player_x, monster_x) > 1800:
            target_loc = 1200
            move_key = "left"
            face_key = "right"
        # 몬스터가 오른쪽에 있을 때는 몬스터의 왼쪽에서 공격한다.
        elif monster_x > player_x:
            # 너무 가까우면 더 왼쪽으로 물러나고 오른쪽을 바라본다.
            if distance < 300:
                target_loc = monster_x - 400
                move_key = "left"
                face_key = "right"
            # 너무 멀면 공격 가능한 거리까지 접근한다.
            elif distance > 800:
                target_loc = monster_x - 700
                move_key = "right"
                face_key = "right"
            else:
                target_loc = player_x
                move_key = "right"
                face_key = "right"
        # 몬스터가 왼쪽에 있을 때는 몬스터의 오른쪽에서 공격한다.
        else:
            if distance < 300:
                target_loc = monster_x + 400
                move_key = "right"
                face_key = "left"
            elif distance > 800:
                target_loc = monster_x + 700
                move_key = "left"
                face_key = "left"
            else:
                target_loc = player_x
                move_key = "left"
                face_key = "left"

        return target_loc, move_key, face_key
            

    def floor_action(self):
        # 로비일 때
        if self.floor == 0:
            if not self.acting:
                pyautogui.click(1300, 850)
                self.start_action()
                self.substate = "ENTER1"
            elif self.substate == "ENTER1" and self.action_done(0.5):
                self.press("enter")
                self.start_action()
                self.substate = "ENTER2"
            elif self.substate == "ENTER2" and self.action_done(0.1):
                self.release("enter")
                self.start_action()
                self.substate = "DONE"
            elif self.substate == "DONE" and self.action_done(1.0):
                self.substate = None
                return State.INIT

        # 33층일 때
        elif self.floor == MAX_FLOOR:
            if not self.acting:
                pyautogui.click(1440, 500)
                self.start_action()
                self.substate = "RIGHT1"
            elif self.substate == "RIGHT1" and self.action_done(0.5):
                self.press("right")
                self.start_action()
                self.substate = "RIGHT2"
            elif self.substate == "RIGHT" and self.action_done(0.1):
                self.release("right")
                self.start_action()
                self.substate = "ENTER1"
            elif self.substate == "ENTER1" and self.action_done(0.1):
                self.press("enter")
                self.start_action()
                self.substate = "ENTER2"
            elif self.substate == "ENTER2" and self.action_done(0.1):
                self.release("enter")
                self.start_action()
                self.substate = "DONE"
            elif self.substate == "DONE" and self.action_done(1.0):
                self.substate = None
                return State.INIT

        # 나가는 길일 때
        elif self.floor == -1:
            return State.MOVE_TO_PORTAL1
        
        # 6의 배수 층일 때
        elif self.floor % 6 == 0:
            if not self.acting:
                pyautogui.click(1440, 500)
                self.start_action()
                self.substate = "ENTER1"
            elif self.substate == "ENTER1" and self.action_done(0.5):
                self.press("enter")
                self.start_action()
                self.substate = "ENTER2"
            elif self.substate == "ENTER2" and self.action_done(0.1):
                self.release("enter")
                self.start_action()
                self.substate = "DONE"
            elif self.substate == "DONE" and self.action_done(1.0):
                self.substate = None
                return State.INIT
        else:
            return State.FIND_MONSTER

    def update(self, screenshot):
        print(self.state.name)
        if is_loading(crop(screenshot, mp_slash_rois[0])):
            return
        
        mp = get_mp(screenshot)
        hp = get_hp(screenshot)
        clear = get_clear(screenshot)
        floor = get_floor(screenshot)
        player_x, player_y, score = get_player(screenshot)

        if player_x is not None:
            self.player = (player_x, player_y)

        elif player_x is None and self.floor % 6 != 0:
            print("플레이어 못찾음")
            return

        priority_state = self.check_priority(mp, hp)
        if priority_state is not None:
            self.state = priority_state
            return

        # state가 몹타격 상태 일 때 1초 이상 지나면 오브젝트의 위치를 다시 찾음
        if self.state == State.ATTACK and (time.monotonic() > self.find_object_start + 1):
            self.find_object_start = time.monotonic()


        if self.state == State.INIT:
            self.reset_floor()
            self.state = State.GET_FLOOR
            return


        if self.state == State.GET_FLOOR:
            if self.floor == floor:
                print("이전층과 같아서 다시 탐색")
            else:
                self.floor = floor
                self.state = State.FLOOR_ACTION
            return


        if self.state == State.FLOOR_ACTION:
            state = self.floor_action()
            if state is not None:
                self.state = state
            return


        if self.state == State.FIND_MONSTER:
            if clear:
                self.action_done()
                self.state = State.MOVE_TO_PORTAL1
                return
            
            monster_x, monster_y, score = get_monster(screenshot)
            if monster_x is not None:
                self.monster = (monster_x, monster_y)
                self.state = State.MOVE_TO_ATTACK
            else:
                print("몬스터 찾는중..")
            return


        if self.state == State.MOVE_TO_ATTACK:
            if clear:
                self.action_done()
                self.state = State.MOVE_TO_PORTAL1
                return
            
            target_loc, move_key, face_key = self.get_loc_dir()
            if not self.acting:
                self.target_loc, self.move_key, self.face_key = target_loc, move_key, face_key
                self.release_all()
                self.press(self.move_key)
                self.start_action()
                self.substate = "MOVING"
            elif self.substate == "MOVING" and abs(self.player[0] - self.target_loc) < 50:
                self.release(self.move_key)
                self.start_action()
                self.substate = "FACING1"
            # 플레이어 위치를 계산했더니 방향이 바뀌어야 하면 바뀐 방향키 누름
            elif self.substate == "MOVING" and self.move_key != move_key:
                print("방향전환")
                self.target_loc, self.move_key, self.face_key = target_loc, move_key, face_key
                self.release_all()
                self.press(self.move_key)
                self.start_action()
            elif self.substate == "FACING1" and self.action_done(0.03):
                self.press(self.face_key)
                self.start_action()
                self.substate = "FACING2"
            elif self.substate == "FACING2" and self.action_done(0.08):
                self.release(self.face_key)
                self.substate = None
                self.target_loc = None
                self.move_key = None
                self.face_key = None
                self.state = State.ATTACK
            return


        if self.state == State.ATTACK:
            if clear:
                self.action_done()
                self.state = State.MOVE_TO_PORTAL1
                return
            
            duration = 1.1 if self.floor <= 11 else 0.5
            if not self.acting:
                self.start_action()
                self.substate = "WAIT"
            elif self.substate == "WAIT" and self.action_done(duration):
                self.press("shift")
                self.start_action()
                self.substate = "WAIT_ATTACK"
            # 1.5초 이상 공격하면 위치를 다시 잡으러 감
            elif self.substate == "WAIT_ATTACK" and self.action_done(1.5):
                self.release("shift")
                self.substate = None
                self.state = State.MOVE_TO_ATTACK
            return


        if self.state == State.MOVE_TO_PORTAL1:

            self.target_loc = 1900 if self.floor == -1 else 2035
            move_key = "right" if self.player[0] < self.target_loc else "left"

            if not self.acting:
                self.move_key = move_key
                self.release_all()
                self.press(self.move_key)
                self.start_action()
                self.substate = "MOVING"
            elif self.substate == "MOVING" and abs(self.player[0] - self.target_loc) < 50:
                self.release(self.move_key)
                self.start_action()
                self.substate = "UP1"
            # 플레이어 위치를 계산했더니 방향이 바뀌어야 하면 바뀐 방향키 누름
            elif self.substate == "MOVING" and self.move_key != move_key:
                self.move_key = move_key
                print("방향전환")
                self.release_all()
                self.press(self.move_key)
                self.start_action()
            elif self.substate == "UP1" and self.action_done(0.08):
                self.press("up")
                self.start_action()
                self.substate = "UP2"
            elif self.substate == "UP2" and self.action_done(0.4):
                self.release("up")
                self.substate = "DONE"
                self.start_action()
                # self.target_loc = None
                # self.move_key = None
            elif self.substate == "DONE" and self.action_done(1):
                self.substate = None
                self.target_loc = None
                self.move_key = None
                self.state = State.MOVE_TO_PORTAL2
            return


        if self.state == State.MOVE_TO_PORTAL2:
            if self.player[1] > 1000:
                self.state = State.MOVE_TO_PORTAL1
                return

            self.target_loc = 1280
            move_key = "right" if self.player[0] < self.target_loc else "left"

            if not self.acting:
                self.move_key = move_key
                self.release_all()
                self.press(self.move_key)
                self.start_action()
                self.substate = "MOVING"
            elif self.substate == "MOVING" and abs(self.player[0] - self.target_loc) < 50:
                self.release(self.move_key)
                self.start_action()
                self.substate = "UP1"
            # 플레이어 위치를 계산했더니 방향이 바뀌어야 하면 바뀐 방향키 누름
            elif self.substate == "MOVING" and self.move_key != move_key:
                self.move_key = move_key
                print("방향전환")
                self.release_all()
                self.press(self.move_key)
                self.start_action()
            elif self.substate == "UP1" and self.action_done(0.08):
                self.press("up")
                self.start_action()
                self.substate = "UP2"
            elif self.substate == "UP2" and self.action_done(0.4):
                self.release("up")
                self.substate = None
                self.target_loc = None
                self.move_key = None
                self.state = State.INIT
            return





def main():
    runner = Runner()
    print("1초 후 시작합니다.")
    time.sleep(1)
    with mss.MSS() as sct:
        while True:
            s = time.time()
            screenshot = get_screenshot(sct)
            runner.update(screenshot)
            # print(time.time()-s)



if __name__ == "__main__":
    main()
