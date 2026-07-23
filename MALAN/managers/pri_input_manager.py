import time

from pynput import keyboard
from pynput.keyboard import Key, KeyCode

from models.state import AutomationState
from tasks.pri_task import ShiftToggleTask, CentaurShiftTask, BuffTask1, BuffTask2, TellHealTask, PressShiftTask
from tasks.common_task import NotebookChannelChangeTask
from tasks.item_task import NotebookPutCiderTask, NotebookCharliTask

class InputManager:
    def __init__(self, automation_manager):
        self.automation_manager = automation_manager
        self.pressed_keys = set()
        self.tellheal_enabled = False
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )

    def normalize_key(self, key):
        # 특수키
        if isinstance(key, keyboard.Key):
            return str(key)

        # 일반 문자키
        try:
            return key.char.lower()

        except AttributeError:
            return str(key)

    def is_pressed(self, *keys):
        return all(k in self.pressed_keys for k in keys)

    def on_press(self, key):
        normalized = self.normalize_key(key)
        self.pressed_keys.add(normalized)
        # print(self.pressed_keys)
        
        if key in (Key.up, Key.left, Key.down, Key.right):
            if self.tellheal_enabled:
                self.automation_manager.start_task(TellHealTask())
        
        elif key == Key.caps_lock:
            self.automation_manager.toggle_task(ShiftToggleTask())
            # self.automation_manager.start_task(CentaurShiftTask())

    def on_release(self, key):
        if key == Key.f4: # 종료
            return False
        elif key == Key.f7:
            self.tellheal_enabled = not self.tellheal_enabled
            self.automation_manager.runner.release(Key.shift_l)
        elif key == Key.f9: # 정지
            self.automation_manager.stop()
            return
        elif key == Key.media_play_pause or key == Key.pause:
                print(self.automation_manager.runner.mouse.position)

        try:
            if key in (Key.up, Key.left, Key.down, Key.right):
                if self.tellheal_enabled:
                    return
                    self.automation_manager.state = AutomationState.IDLE
                    self.automation_manager.start_task(PressShiftTask())

            elif key == Key.f8:
                self.automation_manager.start_task(NotebookChannelChangeTask())
            
            elif key == Key.f12:
                self.automation_manager.start_task(NotebookPutCiderTask())
                # self.automation_manager.start_task(NotebookCharliTask())

            elif (hasattr(key, "vk") and key.vk == 96) or key == Key.insert:
                task = BuffTask1()
                # task = BuffTask2()
                self.automation_manager.start_task(task)
                
            # 키조합 인식
            # elif self.is_pressed("Key.ctrl_l") and (isinstance(key, KeyCode) and key.vk == 65):
            #     task = NotepadTask()
            #     self.automation_manager.start_task(task)

        except AttributeError as e:
            raise e
        
        finally:
            normalized = self.normalize_key(key)
            self.pressed_keys.discard(normalized)

    def start(self):

        self.listener.start()

        print("입력 감지 시작")
        # check_magatia()

        self.listener.join()

        print("종료")

def check_magatia():
    import threading
    import pyautogui as pag
    def task():
        while True:
            try:
                x, y = pag.locateCenterOnScreen("../imgs/magatia.png", confidence=0.95, region=(600, 250, 300, 300))
                keycon = keyboard.Controller()
                keycon.tap(Key.f4)
                keycon.release(Key.shift_l)
            except Exception as e:
                time.sleep(5)
    th = threading.Thread(target=task, daemon=True)
    th.start()