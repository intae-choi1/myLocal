from threading import Thread

import pyautogui as pag
from pynput.keyboard import (
    Key, 
    KeyCode,
)

from 공통.job import (
    king_click,
    skill_roll,
    skill_roll_shift,
    moving_heal,
    tabtab,
    drink,
)

from .job import (
    to_king,
    to_hyung
)



def single_key_action_pressed(event, lock, controller, stores, combis, physics, key):
    args = (event, lock, controller, stores, combis, physics, key)
    
    if key in (Key.up, Key.left, Key.down, Key.right):
        physics['direction'] = key
        
    # 무빙힐 (꾹눌러야됨)
    elif key == KeyCode(char='`'):
        thd = Thread(target=moving_heal, args=(*args,))
        thd.start()


def single_key_action(event, lock, controller, stores, combis, physics, key):
    args = (event, lock, controller, stores, combis, physics, key)
    
    if key == Key.f8:         
        event.clear()
        thd = Thread(target=king_click, args=(*args,))
        thd.start()
    elif key == Key.f9:       # 모든 태스크 종료 (일시 중지)
        if event.is_set():
            event.clear()
            print("king click 활성화")
        else:
            event.set()
            print("king click 비활성화")
            
    # 비영 + 출두
    elif key == Key.end:
        # thd = Thread(target=tabtab, args=(*args,))
        thd = Thread(target=to_king, args=(*args,))
        thd.start()
    # 흉가 출두
    elif key == Key.delete:
        thd = Thread(target=to_hyung, args=(*args, '호룽보'))
        thd.start()
    # 흉가 출두
    elif key == Key.insert:
        thd = Thread(target=to_hyung, args=(*args, '호롱보'))
        thd.start()

    # 저주
    elif key == Key.f1:
        thd = Thread(target=skill_roll, args=(*args, '3'))
        thd.start()
    # 마비
    elif key == Key.f2:
        thd = Thread(target=skill_roll, args=(*args, '6'))
        thd.start()
    # 중독
    elif key == Key.f3:
        thd = Thread(target=skill_roll, args=(*args, '5'))
        thd.start()
    
    elif key == KeyCode(char='p'):
        print(pag.position())
        pass
            

#  키조합에 따라 스킬 시전
def combi_key_action(event, lock, controller, stores, combis, physics, key):
    args = (event, lock, controller, stores, combis, physics, key)
    
    if stores['ctrl'] == combis['ctrl']:
        if stores['2'] == combis['2']: # 비영 + 출두
            pass
            # thd = Thread(target=to_king, args=(*args,))
            # thd.start()
            
        elif stores['3'] == combis['3']: # 저주
            thd = Thread(target=skill_roll, args=(*args, '3'))
            thd.start()
            
        elif stores['4'] == combis['4']: # 절망
            thd = Thread(target=skill_roll_shift, args=(*args, 'd'))
            thd.start()
        
        elif stores['5'] == combis['5']: # 활력
            thd = Thread(target=skill_roll_shift, args=(*args, 's'))
            thd.start()
            
        elif stores['e'] == combis['e']: # ctrl+e 여러번
            if physics['e'] == True:
                physics['e'] = False
                thd = Thread(target=drink, args=(*args,))
                thd.start()





