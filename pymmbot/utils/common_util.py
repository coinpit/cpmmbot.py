import time

current_milli_time = lambda: int(round(time.time() * 1000))

def loop():
    while True:
        time.sleep(100)
