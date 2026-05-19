import pygetwindow as gw
import time

class WindowService:

    @staticmethod
    def get_active_window_title():

        try:

            window = gw.getActiveWindow()

            if window is None:
                return None

            return window.title

        except Exception:

            return None

    # ---------------------------------
    # 특정 문자열 포함 여부
    # ---------------------------------

    @staticmethod
    def is_window_active(keyword):

        title = WindowService.get_active_window_title()

        if title is None:
            return False

        return keyword.lower() in title.lower()
    
time.sleep(5)
print(WindowService.get_active_window_title())