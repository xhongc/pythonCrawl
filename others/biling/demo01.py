import os
import time
import win32gui
import win32api
import win32con
from PIL import Image
from PIL import ImageGrab

# w1 = win32gui.FindWindowEx(0,0,'Qt5QWindowToolSaveBits','nox')        #主界面句柄
# win32gui.SetForegroundWindow(w1)

def LeftClick(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    time.sleep(0.25)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
def SlipClick(x,y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -1)
def Ctrl_V():
    win32api.keybd_event(17, 0, 0, 0)
    win32api.keybd_event(86, 0, 0, 0)
    win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
def talk_one(off):
    LeftClick(90,off)
    time.sleep(0.5)
    LeftClick(346,727)
    time.sleep(0.5)
    LeftClick(328,727)
    time.sleep(0.5)
    #Ctrl_V()
    #LeftClick(386.730)
    LeftClick(18,66)
    time.sleep(0.5)
    LeftClick(18, 66)
    time.sleep(0.)



def main():
    off = 120
    count = 0
    while 1:
        a.talk_one(off)
        off += 55
        count += 1
        if count == 9:
            a.SlipClick(120, 500)
            time.sleep(1)
            a.SlipClick(120, 500)
            time.sleep(1)
            count = 0
            off = 120
            time.sleep(1.3)
def reply_chat():
