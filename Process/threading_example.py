import threading
import time


def t_xc():
    f = open('test.txt', 'a')
    f.write('test_dxc' + '\n')
    time.sleep(1)
    # cjlock.acquire()
    f.close()
    # cjlock.release()


if __name__ == '__main__':
    # cjlock = threading.Lock()
    for i in range(10):
        t = threading.Thread(target=t_xc())
        t.start()
