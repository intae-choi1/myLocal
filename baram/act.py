from threading import Thread

import pyautogui as pag
from pynput.keyboard import (
    Key, 
    KeyCode,
)

from job import (
    king_click,
    skill_4, 
    skill_curse,
    skill_roll, 
    skill_biyoung, 
    moving_heal,
    moving_curse,
    tabtab,
    drink, 
)



def single_key_action_pressed(event, lock, controller, physics, key):
    if key in (Key.up, Key.left, Key.down, Key.right):
        physics['direction'] = key
        
    # 무빙힐 (꾹눌러야됨)
    elif key == KeyCode(char='`'):
        thd = Thread(target=moving_heal, args=(event, lock, controller, physics))
        thd.start()


def single_key_action(event, lock, controller, physics, key):
    if key == Key.f6:         # 왕퀘 받기 시작 (좌측)
        event.clear()
        thd = Thread(target=king_click, args=(event, controller, 1095))
        thd.start()
        
    elif key == Key.f7:         # 왕퀘 받기 시작 (중앙)
        event.clear()
        thd = Thread(target=king_click, args=(event, controller, 960))
        thd.start()
        
    elif key == Key.f8:         # 왕퀘 받기 시작 (우측)
        event.clear()
        thd = Thread(target=king_click, args=(event, controller, 820))
        thd.start()

    elif key == Key.f9:       # 모든 태스크 종료 (일시 중지)
        if event.is_set():
            event.clear()
            print("활성화")
        else:
            event.set()
            print("비활성화")
            
    # 탭탭
    elif key == Key.f1:
        thd = Thread(target=tabtab, args=(event, lock, controller, physics))
        thd.start()
            
    # 혼
    elif key == Key.f2:
        thd = Thread(target=skill_curse, args=(event, controller, physics, '3'))
        thd.start()
    
    # 무빙혼
    elif key == Key.f3:
        thd = Thread(target=moving_curse, args=(event, lock, controller, physics))
        thd.start()
    
    elif key == KeyCode(char='p'):
        # print(pag.position())
        pass
            

#  키조합에 따라 스킬 시전
def combi_key_action(event, controller, physics, stores, combis):
    if stores['ctrl'] == combis['ctrl']:
        if stores['2'] == combis['2']: # 혼
            thd = Thread(target=skill_curse, args=(event, controller, physics, '3'))
            thd.start()
            
        elif stores['3'] == combis['3']: # 활력
            thd = Thread(target=skill_roll, args=(event, controller, 'd'))
            thd.start()
            
        elif stores['4'] == combis['4']: # 파혼술
            thd = Thread(target=skill_roll, args=(event, controller, 's'))
            thd.start()
            
        elif stores['e'] == combis['e']: # ctrl+e 여러번
            if physics['e'] == True:
                physics['e'] = False
                thd = Thread(target=drink, args=(event, controller, physics))
                thd.start()
            
            
def add_combi(stores, physics, key):
    if key == Key.ctrl_l:
        stores['ctrl'].add(key)
        
    elif isinstance(key, KeyCode) and key.vk == 50:
        stores['2'].add(KeyCode(char='2'))
        
    elif isinstance(key, KeyCode) and key.vk == 51:
        stores['3'].add(KeyCode(char='3'))
        
    elif isinstance(key, KeyCode) and key.vk == 52:
        stores['4'].add(KeyCode(char='4'))
        
    elif isinstance(key, KeyCode) and key.vk == 69:
        if physics['e']:
            stores['e'].add(KeyCode(char='e'))
            

def remove_combi(stores, physics, key):
    if key == Key.ctrl_l:
        if key in stores['ctrl']:
            stores['ctrl'].remove(key)
    
    elif isinstance(key, KeyCode) and key.vk == 50:
        c = '2'
        key_ = KeyCode(char=c)
        if key_ in stores[c]:
            stores[c].remove(key_)
            
    elif isinstance(key, KeyCode) and key.vk == 51:
        c = '3'
        key_ = KeyCode(char=c)
        if key_ in stores[c]:
            stores[c].remove(key_)
        
    elif isinstance(key, KeyCode) and key.vk ==52:
        c = '4'
        key_ = KeyCode(char=c)
        if key_ in stores[c]:
            stores[c].remove(key_)
    
    elif isinstance(key, KeyCode) and key.vk == 69:
        c = 'e'
        key_ = KeyCode(char=c)
        if key_ in stores[c]:
            stores[c].remove(key_)