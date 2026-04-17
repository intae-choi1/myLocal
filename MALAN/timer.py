import time
import subprocess
import tkinter as tk
from pynput import keyboard


TIMER_COUNT = 3
COUNTDOWN_TIME = 120
ALERT_TIME = 10
UPDATE_MS = 100  # 0.1초12
# TARGET_KEY = keyboard.Key.f2
TARGET_KEY = keyboard.Key.delete
KOREAN_ORDER = ["", "첫", "두", "세", "네", "다섯", "여섯"]

LOOP_TIME = 31.1
LOOP_KEY = keyboard.Key.f5



format_time = f"{int(COUNTDOWN_TIME)//60:02}:{int(COUNTDOWN_TIME)%60:02}.{int((COUNTDOWN_TIME % 1) * 10)}"
format_time2 = f"{int(LOOP_TIME)//60:02}:{int(LOOP_TIME)%60:02}.{int((LOOP_TIME % 1) * 10)}"


# =========================
# 개별 타이머
# =========================
class TimerRow:
    def __init__(self, parent, index):
        self.index = index
        self.duration = COUNTDOWN_TIME
        self.end_time = None
        self.timer_id = None
        self.running = False
        self.alert_played = False 

        frame = tk.Frame(parent)
        frame.pack(pady=3)

        # 상태 표시 동그라미
        self.indicator = tk.Label(frame, text="●", fg="gray", font=("Arial", 12))
        self.indicator.pack(side="left", padx=3)

        tk.Label(frame, text=f"{index+1}.", width=3).pack(side="left")

        self.label = tk.Label(
            frame,
            text=format_time,
            font=("Consolas", 16),
            width=8,
            fg="blue"
        )
        self.label.pack(side="left")

    def start(self, root):
        self.reset(root)
        self.running = True
        self.end_time = time.perf_counter() + self.duration
        self.update(root)

    def reset(self, root):
        if self.timer_id:
            root.after_cancel(self.timer_id)
        self.running = False
        self.alert_played = False
        self.label.config(text=format_time, fg="blue")

    def update(self, root):
        if not self.running:
            return

        remaining = self.end_time - time.perf_counter()
        if remaining <= 0:
            self.running = False
            self.label.config(text="00:00.0", fg="red")
            return

        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        tenth = int((remaining % 1) * 10)

        color = "red" if remaining <= ALERT_TIME else "blue"
        if remaining <= ALERT_TIME and not self.alert_played:
            self.alert_played = True
            order = KOREAN_ORDER[self.index + 1]
            self.speak(f"{order}번째 타이머 10초 남음", 6)

        self.label.config(text=f"{minutes:02}:{seconds:02}.{tenth}", fg=color)

        self.timer_id = root.after(UPDATE_MS, lambda: self.update(root))

    def speak(self, text, rate=6, volume=100, voice="Microsoft Heami Desktop"):
        ps_script = f"""
        Add-Type -AssemblyName System.Speech;
        $s = New-Object System.Speech.Synthesis.SpeechSynthesizer;
        $s.Rate = {rate};
        $s.Volume = {volume};
        $s.SelectVoice('{voice}');
        $s.Speak('{text}');
        """

        subprocess.Popen(
            ["powershell", "-Command", ps_script],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

# =========================
# 반복 30초 루프 타이머 (F3)
# =========================
class LoopTimerRow:
    def __init__(self, parent):
        self.duration = LOOP_TIME
        self.end_time = None
        self.timer_id = None
        self.running = False

        frame = tk.Frame(parent)
        frame.pack(pady=15)

        tk.Label(frame, text=f"{LOOP_TIME}초 반복:", width=8).pack(side="left")

        self.label = tk.Label(
            frame,
            text=format_time2,
            font=("Consolas", 16),
            width=8,
            fg="purple"
        )
        self.label.pack(side="left")

    # 토글 시작/정지
    def toggle(self, root):
        if self.running:
            self.stop(root)
        else:
            self.start(root)

    def start(self, root):
        self.running = True
        self.end_time = time.perf_counter() + self.duration
        self.update(root)

    def stop(self, root):
        self.running = False
        if self.timer_id:
            root.after_cancel(self.timer_id)

    def update(self, root):
        if not self.running:
            return

        remaining = self.end_time - time.perf_counter()

        # 0초 되면 다시 30초로 재시작 (루프)
        if remaining <= 0:
            self.end_time = time.perf_counter() + self.duration
            remaining = self.duration

        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        tenth = int((remaining % 1) * 10)

        self.label.config(text=f"{minutes:02}:{seconds:02}.{tenth}")

        self.timer_id = root.after(UPDATE_MS, lambda: self.update(root))

# =========================
# 메인 앱
# =========================
class MultiKeyTimerApp:
    def __init__(self, root):
        self.root = root
        root.title("키 타이머")
        root.geometry("200x320")
        root.minsize(200,200)
        root.maxsize(200,400)

        self.target_key = None
        self.next_index = 0

        # ---------------------
        # 키 입력
        # ---------------------
        # top = tk.Frame(root)
        # top.pack(pady=10)

        # tk.Label(top, text="감지 문자: ").pack(side="left")

        # vcmd = (root.register(self.validate_one_char), "%P")
        # self.entry = tk.Entry(top, width=5, validate="key", validatecommand=vcmd)
        # self.entry.pack(side="left", padx=5)

        # tk.Button(top, text="확인", command=self.save_key).pack(side="left")

        # self.info = tk.Label(root, text="저장된 키: 없음")
        # self.info.pack(pady=5)

        # ---------------------
        # 타이머 목록
        # ---------------------
        frame = tk.Frame(root)
        frame.pack(pady=10)

        self.timers = [TimerRow(frame, i) for i in range(TIMER_COUNT)]

        # ---------------------
        # 전체 리셋
        # ---------------------
        tk.Button(root, text="전체 리셋", command=self.reset_all, width=15).pack(pady=10)

        # 루프 타이머
        self.loop_timer = LoopTimerRow(root)

        # ---------------------
        # 전역 키
        # ---------------------
        self.listener = keyboard.Listener(on_release=self.global_key)
        self.listener.start()

    # 1글자 제한
    def validate_one_char(self, P):
        return len(P) <= 1

    # 키 저장
    def save_key(self):
        key = self.entry.get()
        if key:
            self.target_key = key
            self.info.config(text=f"저장된 키: {key}")
            self.entry.delete(0, tk.END)

    # 전역 키
    def global_key(self, key):
        try:
            if (key == TARGET_KEY or 
                (hasattr(key, "char") and key.char == TARGET_KEY)):
                    self.root.after(0, self.activate_next_timer)
            elif key == LOOP_KEY:
                self.root.after(0, lambda: self.loop_timer.toggle(self.root))
        except:
            pass

    # ⭐ 이번에 실행된 타이머 표시
    def activate_next_timer(self):
        idx = self.next_index

        # 타이머 시작
        self.timers[idx].start(self.root)
        # 모든 동그라미 회색
        for t in self.timers:
            t.indicator.config(fg="gray")

        # ⭐ 현재 실행된 것만 초록
        self.timers[idx].indicator.config(fg="green")

        self.next_index = (idx + 1) % TIMER_COUNT

    # 전체 리셋
    def reset_all(self):
        # 타이머 초기화
        for t in self.timers:
            t.reset(self.root)
            t.indicator.config(fg="gray")

        self.next_index = 0

        # self.loop_timer.stop(self.root)



# 실행
root = tk.Tk()
app = MultiKeyTimerApp(root)
root.mainloop()
