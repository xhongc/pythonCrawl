__author__ = 'Administrator'

import threading


class Thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)

        self.start()

