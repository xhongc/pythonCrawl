import threading
import time


def ppp():
    while 1:
        time.sleep(1)
        print('1a')


t = threading.Thread(target=ppp)
t.start()
t.join()
