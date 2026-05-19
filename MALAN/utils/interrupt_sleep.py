
import time


def interruptible_sleep(
    seconds,
    check_func,
    interval=0.05
):

    loops = int(seconds / interval)

    for _ in range(loops):

        check_func()

        time.sleep(interval)