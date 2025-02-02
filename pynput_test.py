from datetime import datetime

from pynput.keyboard import (
    Key,
    Controller as Kc, 
    Listener as Kl,
)



cnt = 0

def on_press(key):
    global cnt
    base1 = datetime(2025, 2, 1, 15, 50, 30)
    base2 = datetime(2025, 2, 1, 15, 51, 30)
    now = datetime.now()
    if base1 <= now and now < base2:
        cnt += 1

def on_release(key):
    print(cnt)
    if key == Key.f4:
        return False
    


listner1 = Kl(on_press=on_press, on_release=on_release,)
listner1.start()
print("start main")
listner1.join()