import threading

lock = threading.Lock()

# LockType 확인 (Python 내부 클래스 기반)
if isinstance(lock, type(threading.Lock)):
    print("이 객체는 threading.Lock입니다.")
else:
    print("이 객체는 threading.Lock이 아닙니다.")
