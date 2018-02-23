#coding=utf-8
import pythoncom
import pyHook
import sys
import ConfigParser
from PIL import ImageGrab
import os
import time

conf = ConfigParser.ConfigParser()
conf.read('auto.conf')
count =1
def onMouseEvent(event):
    # print("MessageName:", event.MessageName)
    # print("Message:", event.Message)
    # print("Time:", event.Time)
    # print("Window:", event.Window)
    # print("WindowName:", event.WindowName)
    # print("Position:", event.Position)
    # print("Wheel:", event.Wheel)
    # print("Injected:", event.Injected)
    # print("---")

    if event.MessageName=="mouse left down":
        x, y = event.Position
        # with open('pyhookconfig.txt','a') as f:
        #     position = event.Position
        #     print(position)
        #     f.write(str(position))
        #     f.write('\n')
        global count
        action = 'action%s'%count
        print action
        conf.set('auto_set',action,str((x,y)))
        count += 1
        conf.write(open("auto.conf", "w"))
        screen(x, y,action)
    elif event.MessageName=="mouse right down":
        sys.exit()

    return True

# def onKeyboardEvent(event):
#     print ("MessageName:", event.MessageName)
#     print ("Message:", event.Message)
#     print("Time:", event.Time)
#     print("Window:", event.Window)
#     print("WindowName:", event.WindowName)
#     print("Ascii:", event.Ascii, chr(event.Ascii))
#     print("Key:", event.Key)
#
#     print("KeyID:", event.KeyID)
#     print("ScanCode:", event.ScanCode)
#     print("Extended:", event.Extended)
#     print("Injected:", event.Injected)
#     print("Alt", event.Alt)
#     print("Transition", event.Transition)
#     print("---")
#     # 同鼠标事件监听函数的返回值
#     return True

def MouseSwitch(event):
    pass
def screen(x,y,action):
    if not os.path.isdir("cature/60x30"):
        os.mkdir("cature/60x30")
    box = (x-30,y-15,x+30,y+15)
    pic = ImageGrab.grab(box)
    pic.save("cature/60x30/" + str(action) + ".png")

def main():
    # 创建一个“钩子”管理对象
    hm = pyHook.HookManager()
    # 监听所有键盘事件
    # hm.KeyDown = onKeyboardEvent
    # 设置键盘“钩子”
    # hm.HookKeyboard()
    # 监听所有鼠标事件
    hm.MouseAll = onMouseEvent

    # 设置鼠标“钩子”
    hm.HookMouse()
    # 进入循环，如不手动关闭，程序将一直处于监听状态
    pythoncom.PumpMessages()


if __name__ == "__main__":
    page = '1'
    money = 250
    money = money + int(page) *10 **(-2)
    print money