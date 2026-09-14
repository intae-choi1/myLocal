import time, pyautogui, cv2, numpy as np
from mss import mss
from enum import Enum, auto


# 상태
class State(Enum):
    INIT = auto()
    FIND_FLOOR = auto()
    FLOOR_ACTION = auto()
    FIND_MONSTER = auto()
    POSITION = auto()
    ATTACK = auto()
    PORTAL = auto()
    NEXT = auto()
    # ERROR = auto()
    # DONE = auto()

# =========================
# 설정
# =========================
sct = mss()
pyautogui.PAUSE=.01

GAME = {"left":300, "top":35, "width":1860, "height":1205}

MINIMAP = (300-GAME["left"], 35-GAME["top"], 50, 25)
FIELD = (400-GAME["left"], 435-GAME["top"], 1760, 840)

PLAYER = "../imgs/mooreung/templates/player.png"
MONSTER = "../imgs/mooreung/templates/monster.png"

CLEAR = (1250-GAME["left"], 700-GAME["top"])
PORTAL = (2035-GAME["left"], 1190-GAME["top"])
PORTAL_EXIT = (1900-GAME["left"], 1190-GAME["top"])

MATCH_PLAYER = 0.8
MATCH_MONSTER = 0.65

TARGET_DIST = 750
DIST_TOL = 20

MAX_FLOOR = 33

# 화면
def screenshot():
    img = np.array(sct.grab(GAME))
    return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

def crop(img, roi):
    x, y, w, h = roi
    return img[y:y+h, x:x+w]

# Template Matching
def match(img, template, threshold=0.7, roi=None):
    if roi:
        base = crop(img, roi)
    else:
        base = img

    temp = cv2.imread(template)

    if temp is None:
        raise FileNotFoundError(template)

    gray = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY)
    temp_gray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(gray, temp_gray, cv2.TM_CCOEFF_NORMED)
    
    _, score, _, pos = cv2.minMaxLoc(result)

    if score<threshold:
        return None

    h, w = temp_gray.shape

    if roi:
        pos=(pos[0]+roi[0], pos[1]+roi[1])

    return (pos[0]+w//2, pos[1]+h//2, score)

def find_player(img):
    r = match(img, PLAYER, MATCH_PLAYER, FIELD)
    return None if r is None else r[:2]

def find_monster(img):
    r = match(img, MONSTER, MATCH_MONSTER, FIELD)
    return None if r is None else r[:2]

def find_clear(img):
    b, g, r = img[CLEAR[1], CLEAR[0]]
    return True if r == 204 else False

# 층 인식
def get_floor(img):
    mm = crop(img, MINIMAP)

    best_floor = None
    best_score = 0

    for floor in range(-1, MAX_FLOOR+1):
        path = f"../imgs/mooreung/floor/{floor}.png"

        r = match(mm, path, 0.5)
        if r and r[2] > best_score:
            best_score = r[2]
            best_floor = floor

    return best_floor

# 포지션 거리 계산
def find_position(player, target):
    dx = target[0]-player[0]
    d = abs(dx)

    if d <= TARGET_DIST + DIST_TOL:
        return True, None
    else:
        direction = "right" if dx > 0 else "left"
        return False, direction

def find_portal(player, floor):
    if player is None:
        return False
    if floor == -1:
        dx = PORTAL_EXIT[0]-player[0]
    else:
        dx = PORTAL[0]-player[0]

    if abs(dx) <= 100:
        return True

    return False

def do_buff(floor):
    pyautogui.keyDown("q")
    time.sleep(0.5)
    pyautogui.keyUp("q")

    pyautogui.keyDown("w")
    time.sleep(1.5)
    pyautogui.keyUp("w")

    pyautogui.keyDown("e")
    time.sleep(0.5)
    pyautogui.keyUp("e")

    pyautogui.keyDown("r")
    time.sleep(0.8)
    pyautogui.keyUp("r")

    pyautogui.keyDown("3")
    time.sleep(0.8)
    pyautogui.keyUp("3")
    if floor == 18:
        pyautogui.keyDown("2")
        time.sleep(0.8)
        pyautogui.keyUp("2")

class Runner:
    def __init__(self):
        self.floor = -2                 # 시작은 없는 층
        self.monster = None             # 몬스터 위치는 1번만 찾는데 저장용
        self.player = None              # 아직 쓸모 없음
        self.find_monster_start = 0     # 몬스터 찾는 시간 기록용
        self.find_monster_timeout = 10  # 몬스터 찾는 최대 시간
        self.attack_start = 0           # 공격 시간 기록 용
        self.attack_timeout = 3         # 공격 최대 시간
        self.action_start = 0           # 액션 시간 기록용
        self.action = None              # SubState 개념
        self.acting = False             # 액션이 진행중인지 확인용
        self.keys = set()               # 눌린 키 모음 세트

    def reset_floor(self):
        self.monster = None
        self.player = None
        self.find_monster_start = 0
        self.attack_start = 0
        self.action = None
        self.acting = False

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

    def update(self):
        global state
        img = screenshot()

        if state==State.INIT:
            self.reset_floor()
            state = State.FIND_FLOOR
            return

        # 층 확인
        if state==State.FIND_FLOOR:
            # 새로 찾은 층이 이전 층이랑 같으면 다시 새로 층을 찾게함
            # 다음화면 넘어가기 전에 get_floor했기 때문
            floor = get_floor(img)
            if self.floor == floor:
                print("이전층과 같아서 다시 탐색")
            else:
                print(f"[FLOOR] {floor}")
                self.floor = floor
                state = State.FLOOR_ACTION
            return
        
        if state==State.FLOOR_ACTION:
            # 로비일 때
            if self.floor == 0:
                if not self.acting:
                    do_buff(self.floor)
                    pyautogui.click(1300, 850)
                    self.start_action()
                    self.action = "ENTER"

                elif self.action == "ENTER" and self.action_done(0.5):
                    pyautogui.press("enter")
                    self.start_action()
                    self.action = "NEXT"

                elif self.action == "NEXT" and self.action_done(1.0):
                    self.action = None
                    state = State.INIT
                return
            # 32층일 때
            elif self.floor == MAX_FLOOR:
                if not self.acting:
                    pyautogui.click(1440, 500)
                    self.start_action()
                    self.action = "RIGHT"

                elif self.action == "RIGHT" and self.action_done(0.5):
                    pyautogui.press("right")
                    self.start_action()
                    self.action = "ENTER"

                elif self.action == "ENTER" and self.action_done(0.05):
                    pyautogui.press("enter")
                    self.start_action()
                    self.action = "NEXT"

                elif self.action == "NEXT" and self.action_done(1.0):
                    self.action = None
                    state = State.INIT
                return
            # 나가는 길일 때
            elif self.floor == -1:
                state = State.PORTAL
                return
            # 6의 배수 층일 때
            elif self.floor % 6 == 0:
                if not self.acting:
                    if self.floor == 18:
                        do_buff(self.floor)
                    pyautogui.click(1440, 500)
                    self.start_action()
                    self.action = "ENTER"

                elif self.action == "ENTER" and self.action_done(0.5):
                    pyautogui.press("enter")
                    self.start_action()
                    self.action = "NEXT"

                elif self.action == "NEXT" and self.action_done(1.0):
                    self.action = None
                    state = State.INIT
                return
            self.find_monster_start = time.monotonic()
            state = State.FIND_MONSTER
            return
        
        # 초기 몬스터 표식 찾기
        if state==State.FIND_MONSTER:
            if self.monster is None:
                monster = find_monster(img)
                if monster:
                    self.monster = monster
                    print(f"[MONSTER] {monster[0]},{monster[1]}")
                    state = State.POSITION
                    return

            if time.monotonic() >= self.find_monster_start + self.find_monster_timeout:
                print("[CLEAR] 오래 몹을 찾지 못해서 포탈 찾기 상태로 이동")
                state = State.PORTAL
                return
            return

        # 캐릭터 위치 조절
        if state==State.POSITION:
            if self.monster is None:
                state = State.FIND_MONSTER
                return
            
            # 몬스터가 왼쪽에서 뜨면 왼쪽으로 붙기 & 어택 상태로 넘어감
            if self.monster[0] < 1000:
                if not self.acting:
                    self.press("left")
                    self.start_action()
                    self.action = "LEFT_RELEASE"

                elif self.action == "LEFT_RELEASE" and self.action_done(0.6):
                    self.release("left")
                    self.start_action()
                    self.action = "RIGHT_PRESS"

                elif self.action == "RIGHT_PRESS" and self.action_done(0.01):
                    self.press("right")
                    self.start_action()
                    self.action = "RIGHT_RELEASE"

                elif self.action == "RIGHT_RELEASE" and self.action_done(0.02):
                    self.release("right")
                    self.start_action()
                    self.action = "END"

                elif self.action == "END" and self.action_done(0.01):
                    print(f"[POSITION2] monster={self.monster}")
                    self.action = None
                    state = State.ATTACK

                return

            player = find_player(img)
            if player is None:
                return

            done, direction = find_position(player, self.monster)
            if not done:
                d = abs(self.monster[0]-player[0])
                if d > TARGET_DIST + DIST_TOL:
                    self.press(direction)
                else:
                    self.release(direction)

            else:
                self.release_all()
                print(f"[POSITION] player={player} monster={self.monster}")
                state = State.ATTACK



        if state==State.ATTACK:
            duration = 0.8 if self.floor <= 11 else 0.5
            if not self.acting:
                self.start_action()
                self.action = "WAIT"

            elif self.action == "WAIT" and self.action_done(duration):
                self.press("shift")
                self.start_action()
                self.action = "ATTACK"

            # ATTACK 상태에서 CLEAR되면 봄 발사
            elif self.action == "ATTACK" and find_clear(img):
                self.action_done()
                self.release("shift")
                self.start_action()
                self.action = "BOMB_PRESS"

            # 3 초간 attack상태면 move상태로 변경
            elif self.action == "ATTACK" and self.action_done(3):
                self.release("shift")
                self.press("right")
                self.start_action()
                self.action = "MOVE"

            # move 상태에서 다시 attack 상태로 복귀
            elif self.action == "MOVE" and self.action_done(0.5):
                self.release("right")
                self.press("shift")
                print("[ERROR] attack timeout and move right")
                self.start_action()
                self.action = "ATTACK"

            elif self.action == "BOMB_PRESS" and self.action_done(0):
                if self.floor == 31:
                    time.sleep(2)
                    self.press("s")
                self.start_action()
                self.action = "BOMB_RELEASE"

            elif self.action == "BOMB_RELEASE" and self.action_done(0.2):
                self.release("s")
                print("[CLEAR]")
                self.action = None
                state = State.PORTAL
            return

        # 포탈
        if state==State.PORTAL:
            if not self.acting:
                self.press("right")
                self.start_action()
                self.action = "FIND"

            elif self.action == "FIND" and find_portal(find_player(img), self.floor):
                self.release("right")
                self.press("up")
                self.start_action()
                self.action = "WAIT_UP"

            elif self.action == "WAIT_UP" and self.action_done(1.2):
                self.release("up")
                print("[PORTAL]")
                self.action = None
                state = State.NEXT
            return

        # 다음 층
        if state==State.NEXT:
            if not self.acting:
                self.start_action()
                self.action = "WAIT"

            elif self.action == "WAIT" and self.action_done(0.2):
                # 포탈을 넘어가지 못했다면 왼쪽으로 이동후 윗방향키
                if self.floor == get_floor(img):
                    self.press("left")
                    self.start_action()
                    self.action = "LEFT_RELEASE"
                else:
                    print("[DONE]")
                    self.action = None
                    state = State.INIT

            elif self.action == "LEFT_RELEASE" and self.action_done(0.5):
                self.release("left")
                self.press("up")
                self.start_action()
                self.action = "UP_RELEASE"

            elif self.action == "UP_RELEASE" and self.action_done(0.5):
                self.release("up")
                self.action = None

            return

            
# 실행
def main():
    global state
    runner = Runner()

    print("2초 후 시작합니다.")
    time.sleep(2)

    state = State.INIT
    while True:
        runner.update()
        time.sleep(0.005)


if __name__=="__main__":
    main()