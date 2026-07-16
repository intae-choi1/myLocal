import random, time
from datetime import datetime, timedelta

import mss
import pyautogui as pag
from pynput.keyboard import Key


sct = mss.mss()


class BuyCiderTask:
    def __init__(self):
        pass

    def run(self, runner):
        for _ in range(9):
            try:
                for i in range(1, 4):
                    if i==3: runner.wait(0.1)
                    x, y = pag.locateCenterOnScreen(f"../imgs/shop_cider_{i}.png", confidence=0.9)
                    runner.move_mouse(x, y, 0.01)
                    runner.click(wait=0.01)
                
            except pag.ImageNotFoundException as e:
                print(e)
                break


class PutCiderTask:
    def __init__(self):
        pass

    def run(self, runner):
        post_stand_x, post_stand_y = pag.locateCenterOnScreen("../imgs/post_meso.png", confidence=0.8)
        cider_stand_x, cider_stand_y = pag.locateCenterOnScreen("../imgs/post_cider.png", confidence=0.8, region=(1480, 40, 1000, 1400))
        for i in range(12):
            try:
                post_x = post_stand_x + 10  + (i%6)*80
                post_y = post_stand_y - 150 + (i//6)*80
                cider_x = cider_stand_x + (i%4)*70
                cider_y = cider_stand_y + (i//4)*70
                runner.move_mouse(cider_x, cider_y, 0.1)
                runner.click(wait=0.15)
                runner.move_mouse(post_x, post_y, 0.04)
                runner.click(wait=0.15)
            except pag.ImageNotFoundException as e:
                print(e)
                break


class NotebookPutCiderTask:
    def __init__(self):
        pass

    def run(self, runner):
        post_stand_x, post_stand_y = pag.locateCenterOnScreen("../imgs/post_meso.png", confidence=0.8)
        cider_stand_x, cider_stand_y = pag.locateCenterOnScreen("../imgs/post_cider.png", confidence=0.8, region=(1300, 300, 500, 700))
        for i in range(7):
            try:
                post_x = post_stand_x + 5  + (i%6)*40
                post_y = post_stand_y - 75 + (i//6)*40
                cider_x = cider_stand_x + (i%4)*35
                cider_y = cider_stand_y + (i//4)*35
                runner.move_mouse(cider_x, cider_y, 0.1)
                runner.click(wait=0.15)
                runner.move_mouse(post_x, post_y, 0.04)
                runner.click(wait=0.15)
            except pag.ImageNotFoundException as e:
                print(e)
                break


class CharliTask:
    def __init__(self):
        pass

    def run(self, runner):
        try:
            charli_x, charli_y = pag.locateCenterOnScreen("../imgs/charli.png", confidence=0.7)
            charli_y -= 20
            for _ in range(18):
                runner.move_mouse(charli_x, charli_y, 0.1)
                runner.click(wait=0.15) # 찰리 클릭
                
                runner.move_mouse(1700, 770, 0.1)
                runner.click(wait=0.15) # 다음 클릭

                runner.move_mouse(1650, 870, 0.1)
                runner.click(wait=0.15) # 예 클릭

                # runner.move_mouse(1100, 750, 0.1) # 루나픽시
                runner.mouse_drag(1760, 470, 1763, 953) # 맨밑으로 드래그
                runner.wait(0.2)

                runner.move_mouse(1100, 450, 0.1) # 헥터
                # runner.move_mouse(1100, 560, 0.1) # 화팽
                runner.click(wait=0.15) # 예 클릭

                runner.move_mouse(1650, 870, 0.1)
                runner.click(wait=0.15) # 예 클릭

                runner.move_mouse(1700, 770, 0.1)
                runner.click(wait=0.15) # 다음 클릭
            
        except pag.ImageNotFoundException as e:
            print(e)
            

class NotebookCharliTask:
    def __init__(self):
        pass

    def run(self, runner):
        try:
            charli_x, charli_y = pag.locateCenterOnScreen("../imgs/charli.png", confidence=0.7)
            charli_y -= 20
            for _ in range(18):
                runner.move_mouse(charli_x, charli_y, 0.1)
                runner.click(wait=0.15) # 찰리 클릭
                
                runner.move_mouse(1700, 770, 0.1)
                runner.click(wait=0.15) # 다음 클릭

                runner.move_mouse(1650, 870, 0.1)
                runner.click(wait=0.15) # 예 클릭

                # runner.move_mouse(1100, 750, 0.1) # 루나픽시
                runner.mouse_drag(1760, 470, 1763, 953) # 맨밑으로 드래그
                runner.wait(0.2)

                runner.move_mouse(1100, 450, 0.1) # 헥터
                # runner.move_mouse(1100, 560, 0.1) # 화팽
                runner.click(wait=0.15) # 예 클릭

                runner.move_mouse(1650, 870, 0.1)
                runner.click(wait=0.15) # 예 클릭

                runner.move_mouse(1700, 770, 0.1)
                runner.click(wait=0.15) # 다음 클릭
            
        except pag.ImageNotFoundException as e:
            print(e)


class DropItemTask:
    def __init__(self):
        pass

    def run(self, runner):
        stand_x, stand_y = pag.locateCenterOnScreen("../imgs/equipment.png", confidence=0.7) #701 455
        for i in range(28):
            try:
                if i < 4:
                    continue
                x = stand_x + 10  + (i%4)*70 + (i//24)*300
                y = stand_y + 70 + (i//4)*70 - (i//24)*420
                runner.move_mouse(x, y, 0.04)
                runner.click(wait=0.1)
                runner.move_mouse(stand_x-100, stand_y, 0.04)
                runner.click(wait=0.2)
                runner.tap(Key.enter)
                runner.wait(0.25)
            except pag.ImageNotFoundException as e:
                print(e)
                break