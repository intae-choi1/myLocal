from pynput import keyboard
from pynput.keyboard import Key, KeyCode

from tasks.boma_task import ShiftToggleTask, JumpSkillTask
from tasks.common_task import ChannelChangeTask, PutCiderTask, FlJumpTask, NotebookPutCiderTask


class InputManager:
    def __init__(self, automation_manager):
        self.automation_manager = automation_manager
        self.pressed_keys = set()
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
        if self.automation_manager.runner.is_typing:
            return
        normalized = self.normalize_key(key)
        self.pressed_keys.add(normalized)
        
        if key == Key.caps_lock:
            self.automation_manager.start_task(ShiftToggleTask())
        
        elif key == Key.f1:
            # return
            self.automation_manager.start_task(FlJumpTask())

        # elif key == KeyCode(char='b'):
        #     self.automation_manager.start_task(JumpSkillTask('x'))

        # elif key == KeyCode(char='n'):
        #     self.automation_manager.start_task(JumpSkillTask('c'))


    def on_release(self, key):
        if key == Key.f4: # 종료
            return False

        elif key == Key.f9: # 정지
            print("긴급 중단")
            self.automation_manager.stop()
            return
        
        elif key == Key.pause:
            print(self.automation_manager.runner.mouse.position)

        
        try:
            if key == Key.f8:
                self.automation_manager.start_task(ChannelChangeTask())

            elif key == Key.insert:
                self.automation_manager.start_task(PutCiderTask())
                
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

        self.listener.join()

        print("종료")