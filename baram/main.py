from functools import partial
from threading import Event, Lock

from pynput.keyboard import (
    Key, 
    KeyCode,
    Controller as Kc, 
    Listener as Kl,
)

from 공통.act import add_combi, remove_combi

# from 도사.act import (
#     single_key_action_pressed,
#     single_key_action, 
#     combi_key_action
# )

from 주술사.act import (
    single_key_action_pressed,
    single_key_action, 
    combi_key_action
)


# 눌릴 때 액션 (꾹누르기 포함)
def on_press(event, lock, controller, stores, combis, physics, key):
    single_key_action_pressed(event, lock, controller, stores, combis, physics, key)
    add_combi(stores, physics, key)
        

# 뗄 때 액션 (단일 명령 및 키조합 명령)
def on_release(event, lock, controller, stores, combis, physics, key):
    # print(f"{key} release.")
    if key == Key.f4:      # 모든 태스크 종료 & 프로그램 종료
        event.set()
        return False
    
    single_key_action(event, lock, controller, stores, combis, physics, key)
    combi_key_action(event, lock, controller, stores, combis, physics, key)

    remove_combi(stores, physics, key)
    
    

if __name__ == "__main__":
    event = Event()
    lock  = Lock()
    key_controller = Kc()
    
    ##############################
    # 키조합에 따른 동작 활성화를 위한 세팅
    # combis에 있는 값과 stores에 있는 값이 일치하면 동작을 활성화함
    # on_press 에서 add_combi하고, on_release에서 remove_combi함
    stores = {
        'ctrl': set(),
        '2': set(),
        '3': set(),
        '4': set(),
        '5': set(),
        'e': set(),
    }
    combis = {
        'ctrl': {Key.ctrl_l},
        '2': {KeyCode(char='2')},
        '3': {KeyCode(char='3')},
        '4': {KeyCode(char='4')},
        '5': {KeyCode(char='5')},
        'e': {KeyCode(char='e')},
    }
    physics = {
        'e': True,
        'toggle': True,
        'direction': Key.right
    }
    ##############################
    
    on_press = partial(on_press, event, lock, key_controller, stores, combis, physics)
    on_release = partial(on_release, event, lock, key_controller, stores, combis, physics)
    
    listner1 = Kl(on_press=on_press, on_release=on_release,)
    listner1.start()
    print("start main")
    listner1.join()

