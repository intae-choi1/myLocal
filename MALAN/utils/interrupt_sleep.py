
import time


def interruptible_sleep(
    seconds,
    check_func,
    interval=0.05
):

    loops = int(seconds // interval)
    last = round(seconds % interval, 3)

    for _ in range(loops):
        check_func()
        time.sleep(interval)

    time.sleep(last)