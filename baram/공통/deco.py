import time
import pyautogui as pag


# 메이플월드일때만 실행 
# lock되지 않았을때만 ← 2번째 인자가 lock객체인 함수에만 적용
# lock걸고 시작, 끝나면 lock 해제
def deco1(func):
    def wrapper(*args, **kwargs):
        # s = time.time()
        w = pag.getActiveWindow()
        if w and w.title.startswith("Maple"):
            lock = args[1]
            if not lock.locked():
                lock.acquire()
                func(*args, **kwargs)
                lock.release()
        # e = time.time()
        # print(f"{func.__name__} {e-s:.5f} seconds elapsed.")
    return wrapper
