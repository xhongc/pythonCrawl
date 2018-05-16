from PyQt5 import QtWidgets
from design_01 import Ui_Dialog
import sys, time, os
import codecs
import os
import time
import win32gui
import win32api
import win32con

global on_off


def LeftClick(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.25)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def SlipClick(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -1)


def Ctrl_V():
    win32api.keybd_event(17, 0, 0, 0)
    win32api.keybd_event(86, 0, 0, 0)
    win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)


def talk_one(off):
    LeftClick(90, off)
    time.sleep(0.8)
    LeftClick(346, 727)
    time.sleep(0.8)
    LeftClick(300, 727)
    time.sleep(1.2)
    # Ctrl_V()
    time.sleep(0.8)
    LeftClick(386, 730)
    time.sleep(0.8)
    LeftClick(18, 66)
    time.sleep(0.8)
    LeftClick(18, 66)
    time.sleep(0.8)


def reply_one(off):
    LeftClick(90, off)
    time.sleep(0.8)
    LeftClick(300, 727)
    time.sleep(1.2)
    # Ctrl_V()
    time.sleep(0.8)
    LeftClick(18, 66)
    time.sleep(0.8)


class Video(QtWidgets.QWidget, Ui_Dialog):
    def __init__(self):
        super(Video, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(self.stop)
        self.pushButton_2.setShortcut('Q')
        self.pushButton_3.clicked.connect(self.reply)

    def start(self):
        off = 120
        count = 0
        on_off = 1
        while on_off:
            try:
                talk_one(off)
            except BaseException as e:
                print(e)
                break
            off += 55
            count += 1
            if count == 9:
                SlipClick(120, 500)
                time.sleep(2)
                SlipClick(120, 500)
                time.sleep(2)
                count = 0
                off = 120
                time.sleep(1.3)

    def stop(self):
        on_off = False

    def reply(self):
        off = 190
        count = 0
        on_off = 1
        while on_off:
            try:
                reply_one(off)
            except BaseException as e:
                print(e)
                break
            off += 70
            count += 1
            if count == 8:
                SlipClick(120, 500)
                time.sleep(2)
                SlipClick(120, 500)
                time.sleep(2)
                count = 0
                off = 120
                time.sleep(1.3)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myshow = Video()
    myshow.show()
    sys.exit(app.exec_())

