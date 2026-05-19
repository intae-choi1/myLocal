from datetime import datetime, timedelta

from pynput.keyboard import Key


class NotepadTask:

    def __init__(self):

        pass

    def run(self, runner):

        print("메모장 작업 시작")

        # ---------------------------------
        # 메모장 더블클릭
        # ---------------------------------

        runner.move_mouse(300, 300)

        runner.double_click()

        # runner.wait(1)

        # ---------------------------------
        # 날짜 계산
        # ---------------------------------
        date = datetime.now()

        text = date.strftime("%Y-%m-%d")

        # ---------------------------------
        # 입력
        # ---------------------------------

        runner.type_text(text)

        runner.wait(0.5)

        # ---------------------------------
        # 저장
        # ---------------------------------


        runner.hotkey(Key.ctrl, "s")

        print("메모장 작업 종료")