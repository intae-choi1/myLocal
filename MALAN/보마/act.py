from threading import Thread

import pyautogui as pag
from pynput.keyboard import (
    Key, 
    KeyCode,
)
from pynput.mouse import Controller as MC

from 공통.job import (
    channel_change,
    skill_roll,
    skill_roll_shift,
    moving_skill,
    moving_heal,
    tabtab,
    drink,
)

from .job import (
    use_shift,
    jump_skill
)


mc = MC()


def single_key_action_pressed(event, lock, controller, stores, combis, physics, key):
    args = (event, lock, controller, stores, combis, physics, key)
    
    if key in (Key.up, Key.left, Key.down, Key.right):
        physics['direction'] = key
        
    # shift 꾹 누르기 (caps_lock으로 토글)
    elif key == Key.caps_lock:
        thd = Thread(target=use_shift, args=(*args,))
        thd.start()

    # elif key == KeyCode(char='b'):
    #     thd = Thread(target=jump_skill, args=(*args,"x"))
    #     thd.start()
    # elif key == KeyCode(char='n'):
    #     thd = Thread(target=jump_skill, args=(*args,"c"))
    #     thd.start()


def single_key_action(event, lock, controller, stores, combis, physics, key):
    args = (event, lock, controller, stores, combis, physics, key)
    
    if key == Key.pause:    # pause 누르면 마우스 포지션 출력
        print(mc.position)

    elif key == Key.f8:         # 채널변경
        event.clear()
        thd = Thread(target=channel_change, args=(*args,))
        thd.start()
    elif key == Key.f9:       # 모든 태스크 종료 (일시 중지)
        if event.is_set():
            event.clear()
        else:
            event.set()
    ## 탭탭
    # elif key == Key.end:
    #     thd = Thread(target=tabtab, args=(*args,))
    #     thd.start()
    # # 무빙혼
    # elif key == Key.f1:
    #     thd = Thread(target=moving_skill, args=(*args, '3'))
    #     thd.start()
    # # 혼
    # elif key == Key.f2:
    #     thd = Thread(target=skill_roll, args=(*args, '3'))
    #     thd.start()
    
    # elif key == KeyCode(char='p'):
    #     # print(pag.position())
    #     pass
            

#  키조합에 따라 스킬 시전
def combi_key_action(event, lock, controller, stores, combis, physics, key):
    args = (event, lock, controller, stores, combis, physics, key)
    return

    if stores['ctrl'] == combis['ctrl']:
        if stores['2'] == combis['2']: # 혼
            thd = Thread(target=skill_roll, args=(*args, '3'))
            thd.start()
            
        elif stores['3'] == combis['3']: # 활력
            thd = Thread(target=skill_roll_shift, args=(*args, 'd'))
            thd.start()
            
        elif stores['4'] == combis['4']: # 파혼술
            thd = Thread(target=skill_roll_shift, args=(*args, 's'))
            thd.start()
            
        elif stores['5'] == combis['5']: # 부활
            thd = Thread(target=revive, args=(*args,))
            thd.start()
            
        elif stores['e'] == combis['e']: # ctrl+e 여러번
            if physics['e'] == True:
                physics['e'] = False
                thd = Thread(target=drink, args=(*args,))
                thd.start()






