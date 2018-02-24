#! python2
#coding=utf-8

__author__ = 'xhongc'

import os
import time
import win32gui
import win32api
import win32con
from PIL import Image
from PIL import ImageGrab,ImageChops
import pythoncom
import pyHook
import sys
import ConfigParser
import pythoncom
import pyHook
import codecs

wdname = u'实时演示'
w1 = win32gui.FindWindow('CPhoneCtrlFrameWindow', wdname)  # 主界面句柄

w2 = win32gui.FindWindowEx(w1, None, 'CPhoneCtrlScreenWindow', None)  # 次界面句柄

w3 = win32gui.FindWindowEx(w1, None, 'ATL:00913F40', None)  # 输入框句柄

win32gui.SetForegroundWindow(w1)

conf = ConfigParser.ConfigParser()
conf.readfp(codecs.open('auto.conf',"r","utf-8-sig"))

count_name =1
# 监控鼠标操作
def onMouseEvent(event):

    if event.MessageName=="mouse left down":
        x, y = event.Position

        global count_name
        action = 'action%s'%count_name
        work_mode = conf.get('work_mode','work_mode')
        if work_mode == 'zhifubao':
            if action == 'action1':
                print u'请点击< 添加收款理由'
                screen(x, y, action)
            elif action == 'action2':
                print u'输入理由后请点击 < 发送'
                screen(x, y, action)
            elif action == 'action3':
                print u'请点击 < 金额输入框'
            elif action == 'action4':
                print u'输入金额后请点击 < 发送'
            elif action == 'action5':
                print u'请点击 < 确定点击在蓝色空区域'
            elif action == 'action6':
                print u'请点击 < 二维码右上角区域'
            elif action == 'action7':
                print u'请点击 < 保存图片'
            elif action == 'action8':
                print u'请点击 < 清楚金额'
            else:
                print u'\n(退出模拟:直接关闭控制台！)'
            conf.set('auto_set',action,str((x,y)))
            count_name += 1
            conf.write(open("auto.conf", "w"))

        elif work_mode == 'weixin':
            if action == 'action1':
                print u'请点击< 添加收钱备注'
                screen(x, y, action)
            elif action == 'action2':
                print u'在弹出的输入框 点击》'
                screen(x, y, action)
            elif action == 'action3':
                screen(x, y, action)
                print u'点击 取消后》直接输入金额》后按下回车'
            elif action == 'action4':
                print u'在确定按钮左绿色区域 点击'
            elif action == 'action5':
                print u'在二维码右上角 黑色中点 》点击'
            elif action == 'action6':
                print u'点击》保存收款码'
            elif action == 'action7':
                print u'点击》清除金额'
            elif action == 'action8':
                print u'关闭控制台 开始work'
            elif action == 'action9':
                print u'关闭控制台 开始work'
            elif action == 'action10':
                print u'退出模拟:直接关闭控制台'
            else:
                print u'\n(退出模拟:直接关闭控制台！)'
            conf.set('auto_set',action,str((x,y)))
            count_name += 1
            conf.write(open("auto.conf", "w"))

    elif event.MessageName=="mouse right down":
        # sys.exit()
        win32api.PostQuitMessage()
    return True

def onKeyboardEvent(event):
    if event.Key == 'Escape':
        sys.exit()
    return True

# 截图保存
def screen(x,y,action):
    if not os.path.isdir("cature/60x30"):
        os.mkdir("cature/60x30")
    box = (x-50,y-15,x+50,y+15)
    pic = ImageGrab.grab(box)
    pic.save("cature/60x30/" + str(action) + ".png")

    if not os.path.isdir("cature/260x160"):
        os.mkdir("cature/260x160")
    box = (x-110,y-75,x+130,y+0)
    pic = ImageGrab.grab(box)
    pic.save("cature/260x160/" + str(action) + ".png")

def main_pyhook():
    # 创建一个“钩子”管理对象
    hm = pyHook.HookManager()
    # 监听所有键盘事件
    hm.KeyDown = onKeyboardEvent
    # 设置键盘“钩子”
    hm.HookKeyboard()
    # 监听所有鼠标事件
    hm.MouseAll = onMouseEvent

    # 设置鼠标“钩子”
    hm.HookMouse()
    # 进入循环，如不手动关闭，程序将一直处于监听状态
    pythoncom.PumpMessages(10000)

def PressOnce(x, y=0):
    win32api.keybd_event(x, 0, y, 0)

# pywin32模拟点击
def LeftClick(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.15)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

# 点击并截图
def LeftClick_with_screen(x,y,local_action,action,size):
    win32api.SetCursorPos((x, y))
    time.sleep(0.2)
    screen(x,y,action)

    im = judge_pic(size,local_action,action)
    im_count = 1
    print im
    while im:
        time.sleep(1)
        screen(x,y,action)
        im = judge_pic(size,local_action,action)
        im_count += 1
        if im_count == 30:
            im_text = u'出现未知错误！当前金额'
            im_a = input(im_text)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.15)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

# 判断截图是否与预设标准一致
def judge_pic(size,local_action,action):
    image1 = Image.open('cature/%s/%s.png'%(size,local_action))
    image2 = Image.open('cature/%s/%s.png'%(size,action))
    im = ImageChops.difference(image1, image2).getbbox()
    return im

# 支付宝保存操作
def save2(money, page):
    int = 1
    time.sleep(0.6)
    while int:
        # 截取图片

        win1 = win32gui.GetWindowDC(w1)
        int = win32gui.GetPixel(win1,read_conf('action7')[0], read_conf('action7')[1])
        #print(int)
        if int:
            time.sleep(0.2)

    LeftClick(read_conf('action8')[0], read_conf('action8')[1])  # 保存图片
    time.sleep(0.4)
    LeftClick(read_conf('action9')[0], read_conf('action9')[1])  # 清楚金额
    # print('tiaoz')
    time.sleep(0.4)

# 读取配置文件处理
def read_conf(action):
    action_conf =conf.get('auto_set',action)
    action_conf = action_conf.replace('(','').replace(')','').replace(' ','').split(',')
    return int(action_conf[0]),int(action_conf[1])

# 支付宝主题操作步骤
def work(money, page):

    LeftClick(read_conf('action1')[0], read_conf('action1')[1])  # 设置金额
    time.sleep(0.8)  # 延时1s
    LeftClick_with_screen(read_conf('action2')[0], read_conf('action2')[1],local_action='action2',action='now2',size='60x30')  # 添加收款理由
    time.sleep(0.4)

    # LeftClick(53, 666)  # 点击输入
    # time.sleep(0.5)
    num = conf.get('settings', 'num')
    no = '-0' + str(page)
    reason = num + '-' + str(money) + no
    #print reason
    # time.sleep(0.2)
    win32api.SendMessage(w3, win32con.WM_SETTEXT, None, str(reason))
    # time.sleep(0.2)

    LeftClick(read_conf('action3')[0], read_conf('action3')[1])  # 点击发送
    time.sleep(0.4)

    LeftClick(read_conf('action4')[0], read_conf('action4')[1])  # 点击输入
    time.sleep(0.4)

    win32api.SendMessage(w3, win32con.WM_SETTEXT, None, str(money))
    time.sleep(0.4)

    LeftClick(read_conf('action5')[0], read_conf('action5')[1])  # 点击发送
    time.sleep(0.4)
    int = 0
    count = 0
    while int != 15371536:

        # time.sleep(0.2)
        win1 = win32gui.GetWindowDC(w1)
        int = win32gui.GetPixel(win1,read_conf('action6')[0], read_conf('action6')[1])  # 获取确定像素
        #print(int)
        if int != 15371536:
            if count == 50:
                count = 0
                b_text = u'长时间确定无响应'
                b = input(b_text)

                # save(money,page)
            else:
                time.sleep(0.2)
                print('wait a moment')
                count +=1


    LeftClick(read_conf('action6')[0], read_conf('action6')[1])  # 点击确定
    time.sleep(0.5)
    save2(money, page)

#微信保存操作
def save_we(money, page):
    int = 1
    time.sleep(0.6)
    while int:
        # 截取图片

        win1 = win32gui.GetWindowDC(w1)
        int = win32gui.GetPixel(win1, read_conf('action6')[0], read_conf('action6')[1])
        print(int)
        if int:
            time.sleep(1)

    LeftClick(read_conf('action7')[0], read_conf('action7')[1])  # 保存图片
    time.sleep(0.5)
    LeftClick(read_conf('action8')[0], read_conf('action8')[1])  # 清楚金额
    # print('tiaoz')
    time.sleep(0.5)

# 微信主体操作步骤
def wechat_work(money,page):
    # s设置金额
    LeftClick_with_screen(read_conf('action1')[0], read_conf('action1')[1],local_action='action1',action='now1',size='60x30')
    time.sleep(0.8)
    # 添加备注
    LeftClick_with_screen(read_conf('action2')[0], read_conf('action2')[1],local_action='action2',action='now2',size='60x30')
    time.sleep(0.8)
    # 备注框中心 谢谢
    LeftClick(read_conf('action3')[0], read_conf('action3')[1])
    time.sleep(0.2)
    # 点击最下方输入框
    #LeftClick(read_conf('action4')[0], read_conf('action4')[1])
    # time.sleep(0.5)
    # # 输入备注
    # num = '237-'  # 修改编号
    # no = '-0' + str(page)
    # reason = num + str(money) + no
    # win32api.SendMessage(w3, win32con.WM_SETTEXT, None, reason)
    # time.sleep(0.4)
    # PressOnce(x=13)
    # 点击确定/quxiao
    LeftClick(read_conf('action4')[0], read_conf('action4')[1])
    time.sleep(0.5)
    # 点击输入
    # LeftClick(read_conf('action4')[0], read_conf('action4')[1])
    # time.sleep(0.4)
    print money,page
    money = money + page *10 **(-2)
    win32api.SendMessage(w3, win32con.WM_SETTEXT, None, str(money))
    PressOnce(x=13)
    # 点击确定
    int = 0
    count = 0
    while int != 1682713:
        # time.sleep(0.2)
        win1 = win32gui.GetWindowDC(w1)
        int = win32gui.GetPixel(win1,read_conf('action5')[0], read_conf('action5')[1])  # 获取确定像素
        print(int)
        if int != 15371536:
            if count == 50:
                count = 0
                b_text = u'长时间确定无响应'
                b = input(b_text)

                # save(money,page)
            else:
                time.sleep(0.2)
                print('wait a moment')
                count +=1
    LeftClick(read_conf('action5')[0], read_conf('action5')[1])  # 点击确定
    time.sleep(0.5)
    save_we(money, page)


# 支付宝金额起始
def main():
    money_01_start = int(conf.get('settings','money_01_start'))
    money_01_end = int(conf.get('settings','money_01_end')) +1
    step = int(conf.get('settings','step'))
    while money_01_start < money_01_end:  # 结束金额
        work(money_01_start, str(1))
        money_01_start += step

    money_02_start = int(conf.get('settings', 'money_02_start'))
    money_02_end = int(conf.get('settings', 'money_02_end')) +1
    while money_02_start < money_02_end:  # 结束金额
        work(money_02_start, str(2))
        money_02_start += step

    money_03_start = int(conf.get('settings', 'money_03_start'))
    money_03_end = int(conf.get('settings', 'money_03_end')) +1
    while money_03_start < money_03_end:  # 结束金额
        work(money_03_start, str(3))
        money_03_start += step

# 微信金额起始
def wechat_main():
    money_01_start = int(conf.get('settings','money_01_start'))
    money_01_end = int(conf.get('settings','money_01_end')) +1
    step = int(conf.get('settings','step'))
    while money_01_start < money_01_end:  # 结束金额
        wechat_work(money_01_start, 1)
        money_01_start += step

    money_02_start = int(conf.get('settings', 'money_02_start'))
    money_02_end = int(conf.get('settings', 'money_02_end')) +1
    while money_02_start < money_02_end:  # 结束金额
        wechat_work(money_02_start, 2)
        money_02_start += step

    money_03_start = int(conf.get('settings', 'money_03_start'))
    money_03_end = int(conf.get('settings', 'money_03_end')) +1
    while money_03_start < money_03_end:  # 结束金额
        wechat_work(money_03_start, 3)
        money_03_start += step

# 支付宝补缺
def que():
    with open(r'que.txt', 'r') as f:
        for each in f.readlines():
            money = each.split('.')[0].split('-')[1]
            page = each.split('.')[0].split('-')[2]
            #print(money, page)
            work(money,str(page))
# 微信补缺
def que_we():
    with open(r'que.txt', 'r') as f:
        for each in f.readlines():
            money = each.split('.')[0].split('-')[1]
            page = each.split('.')[0].split('-')[2]
            #print(money, page)
            wechat_work(money,str(page))

# 模式选择
work_mode = conf.get('work_mode','work_mode')
mode = conf.get('work_mode','mode')
if work_mode == 'zhifubao':

    if mode == 'work':
        time.sleep(1)
        print u'--------开始工作---------'
        main()
    elif mode == 'que':
        que()
    elif mode == 'video':
        time.sleep(1)
        print u'--------开始点击---------'
        main_pyhook()
    else:
        print u'大侠！请重新来过'
elif work_mode == 'weixin':
    if mode =='work':
        time.sleep(1)
        print u'--------开始工作---------'
        wechat_main()
    elif mode == 'que':
        time.sleep(1)
        print u'--------开始工作---------'
        que_we()
    elif mode == 'video':
        time.sleep(1)
        print u'--------开始点击---------'
        main_pyhook()
    else:
        print u'大侠！请重新来过！'
else:
    print u'大侠！请重新来过！'
