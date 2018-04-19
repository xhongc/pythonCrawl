import os
import time
import win32gui
import win32api
import win32con
from PIL import Image
from PIL import ImageGrab

wdname = u'实时演示'
w1 = win32gui.FindWindow('CPhoneCtrlFrameWindow',wdname)        #主界面句柄

w2 = win32gui.FindWindowEx(w1,None,'CPhoneCtrlScreenWindow',None)   #次界面句柄

w3 = win32gui.FindWindowEx(w1, None, 'ATL:00913F40', None)      #输入框句柄

win32gui.SetForegroundWindow(w1)

def PressOnce(x,y=0):
    win32api.keybd_event(x,0,y,0)

def LeftClick(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    time.sleep(0.25)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def work(money,page):

    LeftClick(122,363) #设置金额
    time.sleep(0.5)     #延时1s
    LeftClick(288, 176)  # 添加收款理由
    time.sleep(0.5)

    # LeftClick(53, 666)  # 点击输入
    # time.sleep(0.5)
    num = '211-'         # 修改编号
    no = '-0' + page
    reason = num + money + no
    time.sleep(0.5)
    win32api.SendMessage(w3, win32con.WM_SETTEXT, None, reason)
    time.sleep(0.5)

    LeftClick(304, 666)  #点击发送
    time.sleep(1)

    LeftClick(102,140)   #点击输入
    time.sleep(0.5)

    win32api.SendMessage(w3, win32con.WM_SETTEXT, None, money)
    time.sleep(0.5)

    LeftClick(304,666)    #点击发送
    time.sleep(0.5)

    LeftClick(160,240)  #点击确定
    time.sleep(2.5)

    # 截取图片
    bbox = (50, 117, 280, 425)  #截取范围
    img = ImageGrab.grab(bbox)
    jpgname = str(reason) + '.png'
    img.save(jpgname)

    # time.sleep(2)
    # LeftClick(224, 455) #保存图片

    time.sleep(1)
    LeftClick(122, 435)     #清楚金额
    time.sleep(1)


def main(page):
    money = 1  # 起始金额
    while money < 1001:  #结束金额
        work(str(money), str(page))
        money +=1


for page in range(1,4):
    main(page)