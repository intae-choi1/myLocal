import threading

import pygetwindow as gw

from models.state import AutomationState

from controllers.stop_controller import StopController

from runners.action_runner import ActionRunner

class AutomationManager:
    def __init__(self):
        self.state = AutomationState.IDLE

        self.lock = threading.Lock()

        self.thread = None

        self.stop_controller = StopController()

        self.runner = ActionRunner(
            self.stop_controller
        )


    # ---------------------------------
    # 실행 가능 여부
    # ---------------------------------
    def can_start(self):
        window = gw.getActiveWindow()
        title = ""
        if window is not None:
            title = window.title
        return (self.state == AutomationState.IDLE and title.startswith("Maple"))


    # ---------------------------------
    # Task 시작
    # ---------------------------------
    def start_task(self, task):
        with self.lock:
            if not self.can_start():
                return

            self.state = AutomationState.RUNNING

            self.stop_controller.reset()

            self.thread = threading.Thread(
                target=self._run_task,
                args=(task,),
                daemon=True
            )

            self.thread.start()


    # ---------------------------------
    # 실제 실행
    # ---------------------------------
    def _run_task(self, task):
        try:
            task.run(self.runner)

        except InterruptedError:
            print("작업 중단")

        except Exception as e:
            print("오류 발생:", e)

        finally:
            self.state = AutomationState.IDLE
            self.stop_controller.reset()


    # ---------------------------------
    # 중단
    # ---------------------------------
    def stop(self):
        if self.state == AutomationState.RUNNING:
            self.state = AutomationState.STOPPING
            self.stop_controller.stop()