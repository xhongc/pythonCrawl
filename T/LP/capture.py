#! /usr/bin/env python
#coding=utf8
import os,time,sys
import pythoncom,pyHook,win32api,win32com,win32con,win32clipboard
from PIL import ImageGrab

def onMouseEvent(event):
    # 监听鼠标事件
    print ("MessageName:", event.MessageName)
    # print "Message:", event.Message
    # print "Time:", event.Time
    # print "Window:", event.Window
    # print "WindowName:", event.WindowName
    x,y=event.Position
    print ("Position:", event.Position)
    # print "Wheel:", event.Wheel
    # print "Injected:", event.Injected
    print ("---")
    if event.MessageName=="mouse left down":
        Screen_cap(x,y)
    elif event.MessageName=="mouse right down":
        sys.exit()
    # 返回 True 以便将事件传给其它处理程序
    # 注意，这儿如果返回 False ，则鼠标事件将被全部拦截
    # 也就是说你的鼠标看起来会僵在那儿，似乎失去响应了
    return True


def onKeyboardEvent(event):
    # 监听键盘事件
    print ("MessageName:", event.MessageName)
    print ("Message:", event.Message)
    print ("Time:", event.Time)
    print ("Window:", event.Window)
    print ("WindowName:", event.WindowName)
    print ("Ascii:", event.Ascii, chr(event.Ascii))
    print ("Key:", event.Key)
    print ("KeyID:", event.KeyID)
    print ("ScanCode:", event.ScanCode)
    print ("Extended:", event.Extended)
    print ("Injected:", event.Injected)
    print ("Alt", event.Alt)
    print ("Transition", event.Transition)
    print ("---")

    # 同鼠标事件监听函数的返回值
    return True
def main():
    if not os.path.isdir("capture"):
        os.mkdir("capture")
    # 创建一个“钩子”管理对象
    hm = pyHook.HookManager()
    # 监听所有键盘事件
    hm.KeyDown = onKeyboardEvent
    # 设置键盘“钩子”asdbwsdasdgsdfSaA
    hm.HookKeyboard()
    # 监听所有鼠标事件
    hm.MouseAll = onMouseEvent
    # 设置鼠标“钩子”
    hm.HookMouse()
    # 进入循环，如不手动关闭，程序将一直处于监听状态
    pythoncom.PumpMessages()

def Screen_cap20x10(x,y):
    if not os.path.isdir("capture/20x10"):
        os.mkdir("capture/20x10")
    nametime=time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))
    boxs=(x-10,y-5,x+10,y+5)
    pic = ImageGrab.grab(boxs)
    pic.save( "capture/20x10/"+nametime + ".png")
def Screen_cap30x30(x,y):
    if not os.path.isdir("capture/30x30"):
        os.mkdir("capture/30x30")
    nametime=time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))
    boxs=(x-15,y-15,x+15,y+15)
    pic = ImageGrab.grab(boxs)
    pic.save( "capture/30x30/"+nametime + ".png")
def Screen_cap60x30(x,y):
    if not os.path.isdir("capture/60x30"):
        os.mkdir("capture/60x30")
    nametime=time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))
    boxs=(x-30,y-15,x+30,y+15)
    pic = ImageGrab.grab(boxs)
    pic.save( "capture/60x30/"+nametime + ".png")
def Screen_cap60x60(x,y):
    if not os.path.isdir("capture/60x60"):
        os.mkdir("capture/60x60")
    nametime=time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))
    boxs=(x-30,y-30,x+30,y+30)
    pic = ImageGrab.grab(boxs)
    pic.save( "capture/60x60/"+nametime + ".png")
def Screen_cap120x60(x,y):
    if not os.path.isdir("capture/120x60"):
        os.mkdir("capture/120x60")
    nametime=time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))
    boxs=(x-60,y-30,x+60,y+30)
    pic = ImageGrab.grab(boxs)
    pic.save( "capture/120x60/"+nametime + ".png")
def Screen_cap(x,y):
    Screen_cap30x30(x,y)
    Screen_cap20x10(x,y)
    Screen_cap60x30(x,y)
    Screen_cap60x60(x,y)
    Screen_cap120x60(x,y)



if __name__ == "__main__":
    main()