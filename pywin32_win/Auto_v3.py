__author__ = 'xhongc'

import os
import time
import win32gui
import win32api
import win32con
from PIL import Image
from PIL import ImageGrab, ImageChops
import pythoncom
import pyHook
import sys
import configparser
import pythoncom
import pyHook
import codecs
import random
from random_name import ALL_ENG_NAMES
import pyttsx3
from screenshot import window_capture

# wdname = u'夜神模拟器'
# w1 = win32gui.FindWindow('Qt5QWindowIcon', wdname)  # 主界面句柄
# print(w1)
# w2 = win32gui.FindWindowEx(w1, None, 'Qt5QWindowIcon', None)  # 次界面句柄
# print(w2)
# # w3 = win32gui.FindWindowEx(w1, None, 'ATL:00913F40', None)  # 输入框句柄
#
# win32gui.SetForegroundWindow(w1)
# win32gui.SetWindowPos(w1, win32con.HWND_TOPMOST, 0, 0, 1030, 612,
#                       win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW)
conf = configparser.ConfigParser()
conf.readfp(codecs.open('auto.conf', "r", "utf-8-sig"))

count_name = 1
vk_code = {
    '.': 0xBE,
    '0': 0x30,
    '1': 0x31,
    '2': 0x32,
    '3': 0x33,
    '4': 0x34,
    '5': 0x35,
    '6': 0x36,
    '7': 0x37,
    '8': 0x38,
    '9': 0x39,
    'a': 0x41,
    'b': 0x42,
    'c': 0x43,
    'd': 0x44,
    'e': 0x45,
    'f': 0x46,
    'g': 0x47,
    'h': 0x48,
    'i': 0x49,
    'j': 0x4A,
    'k': 0x4B,
    'l': 0x4C,
    'm': 0x4D,
    'n': 0x4E,
    'o': 0x4F,
    'p': 0x50,
    'q': 0x51,
    'r': 0x52,
    's': 0x53,
    't': 0x54,
    'u': 0x55,
    'v': 0x56,
    'w': 0x57,
    'x': 0x58,
    'y': 0x59,
    'z': 0x5A,
}


def at_code():
    win32api.keybd_event(0xA0, 0, 0, 0)  # shift左
    win32api.keybd_event(0x32, 0, 0, 0)  # -
    win32api.keybd_event(0x32, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
    win32api.keybd_event(0xA0, 0, win32con.KEYEVENTF_KEYUP, 0)


# 截图保存
def screen(x, y, action):
    if not os.path.isdir("cature/60x30"):
        os.mkdir("cature/60x30")
    box = (x - 23, y - 20, x + 23, y + 20)
    pic = ImageGrab.grab(box)
    pic.save("cature/60x30/" + str(action) + ".png")

    # if not os.path.isdir("cature/260x160"):
    #     os.mkdir("cature/260x160")
    # box = (x - 110, y - 75, x + 130, y + 0)
    # pic = ImageGrab.grab(box)
    # pic.save("cature/260x160/" + str(action) + ".png")


def PressOnce(x, y=0):
    win32api.keybd_event(x, 0, y, 0)


# pywin32模拟点击
def LeftClick(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.15)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def LeftSnap(x, y, z, r):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.5)
    win32api.SetCursorPos((z, r))
    time.sleep(1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, z, r, 0, 0)


def LeftSnap2(x, y, z, r):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.SetCursorPos((675, 730))
    time.sleep(0.5)
    win32api.SetCursorPos((675, 630))
    time.sleep(0.5)
    win32api.SetCursorPos((675, 620))
    time.sleep(0.5)
    win32api.SetCursorPos((675, 609))
    time.sleep(0.5)
    win32api.SetCursorPos((675, 594))
    time.sleep(0.5)

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


# 点击并截图
def LeftClick_with_screen(x, y, local_action, action, size):
    win32api.SetCursorPos((x, y))
    time.sleep(0.2)
    screen(x, y, action)

    im = judge_pic(size, local_action, action)
    im_count = 1
    print(im)
    while im:
        time.sleep(1)
        screen(x, y, action)
        im = judge_pic(size, local_action, action)
        im_count += 1
        if im_count == 30:
            im_text = u'出现未知错误！'
            im_a = input(im_text)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.15)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


# 判断截图是否与预设标准一致
def judge_pic(size, local_action, action):
    image1 = Image.open('cature/%s/%s.png' % (size, local_action))
    image2 = Image.open('cature/%s/%s.png' % (size, action))
    im = ImageChops.difference(image1, image2).getbbox()
    return im


# 读取配置文件处理
def read_conf(action):
    action_conf = conf.get('auto_set', action)
    action_conf = action_conf.replace('(', '').replace(')', '').replace(' ', '').split(',')
    return int(action_conf[0]), int(action_conf[1])


def change_user(username):
    print('切换账号！')
    LeftClick(read_conf('action1')[0], read_conf('action1')[1])
    time.sleep(0.8)  # 延时1s
    # LeftClick_with_screen(read_conf('action2')[0], read_conf('action2')[1], local_action='action2', action='now2',
    #                       size='60x30')
    LeftClick(read_conf('action2')[0], read_conf('action2')[1])
    time.sleep(0.4)
    LeftClick(read_conf('action3')[0], read_conf('action3')[1])
    time.sleep(1)

    for each in username:
        PressOnce(vk_code[each])
        time.sleep(0.06)
    at_code()
    for j in 'qq.com':
        PressOnce(vk_code[j])
        time.sleep(0.1)
    time.sleep(1)
    LeftClick(read_conf('action4')[0], read_conf('action4')[1])
    for pwd in 'chao123456789..':
        time.sleep(0.05)
        PressOnce(vk_code[pwd])
    time.sleep(0.8)
    LeftClick(read_conf('action5')[0], read_conf('action5')[1])


def join_gonghui():
    print('加入公会')
    LeftClick(read_conf('action6')[0], read_conf('action6')[1])
    time.sleep(3)
    LeftClick(read_conf('action7')[0], read_conf('action7')[1])
    time.sleep(1.5)
    LeftClick(read_conf('action8')[0], read_conf('action8')[1])
    time.sleep(1)
    for j in '46':
        PressOnce(vk_code[j])
        time.sleep(0.1)
    LeftClick(read_conf('action9')[0], read_conf('action9')[1])
    time.sleep(1)
    LeftClick(read_conf('action10')[0], read_conf('action10')[1])
    time.sleep(1)
    LeftClick(read_conf('action11')[0], read_conf('action11')[1])
    time.sleep(1)


def click_gonghui():
    print('公会一系列操作！')
    # LeftClick_with_screen(read_conf('action6')[0], read_conf('action6')[1], local_action='action6', action='now6',
    #                        size='60x30')
    LeftClick(read_conf('action6')[0], read_conf('action6')[1])
    time.sleep(1)
    LeftClick(read_conf('action13')[0], read_conf('action13')[1])
    time.sleep(1)
    LeftClick(read_conf('action12')[0], read_conf('action12')[1])
    time.sleep(1)
    LeftClick(read_conf('action14')[0], read_conf('action14')[1])
    time.sleep(3)

    LeftClick(read_conf('action14.1')[0], read_conf('action14.1')[1])
    time.sleep(2)
    LeftClick(read_conf('action14.2')[0], read_conf('action14.2')[1])
    time.sleep(1)

    LeftClick(read_conf('action15')[0], read_conf('action15')[1])
    time.sleep(1)
    LeftClick(read_conf('action16')[0], read_conf('action16')[1])
    time.sleep(1)
    LeftClick(read_conf('action17')[0], read_conf('action17')[1])
    time.sleep(1)
    LeftClick(read_conf('action18')[0], read_conf('action18')[1])
    time.sleep(1)
    # guanbi huitui
    # LeftClick(read_conf('action19')[0], read_conf('action19')[1])
    # time.sleep(1)
    # LeftClick(read_conf('action20')[0], read_conf('action20')[1])
    # time.sleep(1)
    donate_money()
    quit_gonghui()


def quit_gonghui():
    print('退出公会！')
    LeftClick(read_conf('action21')[0], read_conf('action21')[1])
    time.sleep(1)
    LeftClick(read_conf('action22')[0], read_conf('action22')[1])
    time.sleep(1)


def donate_money():
    print('捐赠金币！')
    LeftClick(read_conf('action21.1')[0], read_conf('action21.1')[1])
    time.sleep(1)
    LeftClick(read_conf('action21.3')[0], read_conf('action21.3')[1])
    time.sleep(1)
    for _ in range(9):
        LeftClick(read_conf('action21.2')[0], read_conf('action21.2')[1])
        time.sleep(0.3)
    LeftClick(read_conf('action19')[0], read_conf('action19')[1])
    time.sleep(1)
    LeftClick(read_conf('action20')[0], read_conf('action20')[1])
    time.sleep(1)


def exp_get():
    print('获取经验')
    LeftClick(read_conf('action86')[0], read_conf('action86')[1])
    time.sleep(2)
    LeftClick(read_conf('action87')[0], read_conf('action87')[1])
    time.sleep(3)
    LeftClick(read_conf('action20')[0], read_conf('action20')[1])
    time.sleep(2)
    LeftClick(read_conf('action88')[0], read_conf('action88')[1])
    time.sleep(1.4)


def clear_buffer():
    print('清除缓存！')
    LeftClick(read_conf('action89')[0], read_conf('action89')[1])
    time.sleep(1.4)
    LeftClick(read_conf('action90')[0], read_conf('action90')[1])
    time.sleep(1.4)
    LeftClick(read_conf('action91')[0], read_conf('action91')[1])
    time.sleep(1.4)
    LeftClick(read_conf('action92')[0], read_conf('action92')[1])
    time.sleep(1.4)
    LeftClick(read_conf('action93')[0], read_conf('action93')[1])
    time.sleep(1.4)
    LeftClick(read_conf('action94')[0], read_conf('action94')[1])
    time.sleep(1.4)
    LeftClick(read_conf('action96')[0], read_conf('action96')[1])
    time.sleep(5)
    LeftClick(read_conf('action95')[0], read_conf('action95')[1])
    time.sleep(15)
    LeftClick(read_conf('action97')[0], read_conf('action97')[1])
    time.sleep(10)
    LeftClick(read_conf('action98')[0], read_conf('action98')[1])
    time.sleep(2)
    LeftClick(read_conf('action24')[0], read_conf('action24')[1])
    time.sleep(1)


def register(name):
    print('开场过动画开始！')
    # LeftClick(read_conf('action23')[0], read_conf('action23')[1])
    # time.sleep(25)
    LeftClick(read_conf('action24')[0], read_conf('action24')[1])
    time.sleep(1)
    LeftClick(read_conf('action24')[0], read_conf('action24')[1])
    time.sleep(1)
    LeftClick(read_conf('action25')[0], read_conf('action25')[1])
    time.sleep(1)
    ra_name = random.choice(ALL_ENG_NAMES)
    for j in ra_name:
        j = j.lower()
        PressOnce(vk_code[j])
        time.sleep(0.1)
    # for i in name[-2:]:
    #     PressOnce(vk_code[i])
    #     time.sleep(0.1)
    time.sleep(1)
    LeftClick(read_conf('action27')[0], read_conf('action27')[1])
    time.sleep(1)
    LeftClick(read_conf('action24')[0], read_conf('action24')[1])
    time.sleep(1)

    LeftClick(read_conf('action28')[0], read_conf('action28')[1])
    time.sleep(1)
    LeftClick(read_conf('action24')[0], read_conf('action24')[1])
    time.sleep(1)
    LeftClick(read_conf('action29')[0], read_conf('action29')[1])
    time.sleep(1)
    LeftClick(read_conf('action24')[0], read_conf('action24')[1])
    time.sleep(1)
    LeftClick(read_conf('action30')[0], read_conf('action30')[1])
    time.sleep(1)
    LeftClick(read_conf('action24')[0], read_conf('action24')[1])
    time.sleep(1)
    LeftClick(read_conf('action31')[0], read_conf('action31')[1])
    time.sleep(1)
    LeftClick(read_conf('action24')[0], read_conf('action24')[1])
    time.sleep(1)
    LeftClick(read_conf('action30')[0], read_conf('action30')[1])
    time.sleep(1)

    LeftClick(read_conf('action32')[0], read_conf('action32')[1])
    time.sleep(1)
    LeftClick(read_conf('action24')[0], read_conf('action24')[1])
    time.sleep(1)
    LeftClick(read_conf('action33')[0], read_conf('action33')[1])
    time.sleep(1)
    LeftClick(read_conf('action34')[0], read_conf('action34')[1])
    time.sleep(1)

    LeftClick(read_conf('action35')[0], read_conf('action35')[1])
    time.sleep(1)
    LeftClick(read_conf('action36')[0], read_conf('action36')[1])
    time.sleep(1)
    LeftClick(read_conf('action37')[0], read_conf('action37')[1])
    time.sleep(6)
    LeftClick(read_conf('action38')[0], read_conf('action38')[1])
    time.sleep(1)

    LeftClick(read_conf('action35')[0], read_conf('action35')[1])
    time.sleep(1)
    LeftClick(read_conf('action36')[0], read_conf('action36')[1])
    time.sleep(1)
    LeftClick(read_conf('action39')[0], read_conf('action39')[1])
    time.sleep(4)
    LeftClick(read_conf('action24')[0], read_conf('action24')[1])
    time.sleep(1)

    LeftClick(read_conf('action40')[0], read_conf('action40')[1])
    time.sleep(3)
    LeftClick(read_conf('action41')[0], read_conf('action41')[1])
    time.sleep(1)
    LeftClick(read_conf('action24')[0], read_conf('action24')[1])
    time.sleep(1)
    LeftClick(read_conf('action24')[0], read_conf('action24')[1])
    time.sleep(1)
    LeftClick(read_conf('action24')[0], read_conf('action24')[1])
    time.sleep(1)
    LeftClick(read_conf('action24')[0], read_conf('action24')[1])
    time.sleep(18)

    LeftClick(read_conf('action42')[0], read_conf('action42')[1])
    time.sleep(2)
    LeftClick(read_conf('action32')[0], read_conf('action32')[1])
    time.sleep(1)

    LeftClick(read_conf('action43')[0], read_conf('action43')[1])
    time.sleep(1)
    LeftClick(read_conf('action44')[0], read_conf('action44')[1])
    time.sleep(1)
    LeftClick(read_conf('action45')[0], read_conf('action45')[1])
    time.sleep(1)
    LeftClick(read_conf('action46')[0], read_conf('action46')[1])
    time.sleep(1)
    LeftClick(read_conf('action47')[0], read_conf('action47')[1])
    time.sleep(1)
    LeftClick(read_conf('action48')[0], read_conf('action48')[1])
    time.sleep(1)
    LeftClick(read_conf('action32')[0], read_conf('action32')[1])
    time.sleep(1)

    LeftClick(read_conf('action49')[0], read_conf('action49')[1])
    time.sleep(1)
    LeftClick(read_conf('action24')[0], read_conf('action24')[1])
    time.sleep(1)
    LeftClick(read_conf('action50')[0], read_conf('action50')[1])
    time.sleep(1)
    LeftClick(read_conf('action51')[0], read_conf('action51')[1])
    time.sleep(1)
    LeftClick(read_conf('action52')[0], read_conf('action52')[1])
    time.sleep(1)

    LeftClick(read_conf('action32')[0], read_conf('action32')[1])
    time.sleep(1)
    LeftClick(read_conf('action53')[0], read_conf('action53')[1])
    time.sleep(1)
    LeftClick(read_conf('action54')[0], read_conf('action54')[1])
    time.sleep(1)
    for _ in range(5):
        LeftClick(read_conf('action55')[0], read_conf('action55')[1])
        time.sleep(0.2)

    LeftClick(read_conf('action56')[0], read_conf('action56')[1])
    time.sleep(1)
    LeftClick(read_conf('action57')[0], read_conf('action57')[1])
    time.sleep(1)
    LeftClick(read_conf('action58')[0], read_conf('action58')[1])
    time.sleep(1)
    LeftClick(read_conf('action59')[0], read_conf('action59')[1])
    time.sleep(1)
    LeftClick(read_conf('action24')[0], read_conf('action24')[1])
    time.sleep(1)
    LeftClick(read_conf('action32')[0], read_conf('action32')[1])
    time.sleep(1)
    LeftClick(read_conf('action32')[0], read_conf('action32')[1])
    time.sleep(1)
    LeftClick(read_conf('action33')[0], read_conf('action33')[1])
    time.sleep(1)
    LeftClick(read_conf('action34')[0], read_conf('action34')[1])
    time.sleep(1)

    LeftClick(read_conf('action60')[0], read_conf('action60')[1])
    time.sleep(1)
    LeftClick(read_conf('action37')[0], read_conf('action37')[1])
    time.sleep(1)
    LeftClick(read_conf('action61')[0], read_conf('action61')[1])
    time.sleep(1)
    LeftClick(read_conf('action62')[0], read_conf('action62')[1])
    time.sleep(10)

    LeftClick(read_conf('action63')[0], read_conf('action63')[1])
    time.sleep(4)
    LeftClick(read_conf('action24')[0], read_conf('action24')[1])
    time.sleep(0.66)
    LeftClick(read_conf('action24')[0], read_conf('action24')[1])
    time.sleep(0.66)
    LeftClick(read_conf('action24')[0], read_conf('action24')[1])
    time.sleep(0.66)

    LeftClick(read_conf('action38')[0], read_conf('action38')[1])
    time.sleep(1)
    LeftClick(read_conf('action60')[0], read_conf('action60')[1])
    time.sleep(1)
    LeftSnap(410, 490, 209, 490)
    LeftClick(read_conf('action39')[0], read_conf('action39')[1])
    time.sleep(20)
    LeftClick(read_conf('action24')[0], read_conf('action24')[1])
    time.sleep(1)
    LeftClick(read_conf('action63')[0], read_conf('action63')[1])
    time.sleep(5)
    LeftClick(read_conf('action24')[0], read_conf('action24')[1])
    time.sleep(1)

    LeftClick(read_conf('action65')[0], read_conf('action65')[1])
    time.sleep(1)
    LeftClick(read_conf('action62')[0], read_conf('action62')[1])
    time.sleep(1)

    LeftClick(read_conf('action24')[0], read_conf('action24')[1])
    time.sleep(1)
    LeftClick(read_conf('action32')[0], read_conf('action32')[1])
    time.sleep(1)

    LeftClick(read_conf('action66')[0], read_conf('action66')[1])
    time.sleep(1)
    LeftClick(read_conf('action67')[0], read_conf('action67')[1])
    time.sleep(1)
    LeftClick(read_conf('action68')[0], read_conf('action68')[1])
    time.sleep(1)
    LeftClick(read_conf('action69')[0], read_conf('action69')[1])
    time.sleep(1)
    LeftClick(read_conf('action70')[0], read_conf('action70')[1])
    time.sleep(1)

    LeftClick(read_conf('action71')[0], read_conf('action71')[1])
    time.sleep(1)
    LeftClick(read_conf('action72')[0], read_conf('action72')[1])
    time.sleep(1)
    LeftClick(read_conf('action73')[0], read_conf('action73')[1])
    time.sleep(1)
    LeftClick(read_conf('action69')[0], read_conf('action69')[1])
    time.sleep(1)

    LeftClick(read_conf('action32')[0], read_conf('action32')[1])
    time.sleep(1)

    LeftClick(read_conf('action74')[0], read_conf('action74')[1])
    time.sleep(1)

    LeftClick(read_conf('action31')[0], read_conf('action31')[1])
    time.sleep(1)
    LeftClick(read_conf('action24')[0], read_conf('action24')[1])
    time.sleep(1)
    LeftClick(read_conf('action30')[0], read_conf('action30')[1])
    time.sleep(1)

    LeftClick(read_conf('action32')[0], read_conf('action32')[1])
    time.sleep(1)

    LeftClick(read_conf('action24')[0], read_conf('action24')[1])
    time.sleep(1)
    LeftClick(read_conf('action24')[0], read_conf('action24')[1])
    time.sleep(1)


def register_username(username):
    print('填写注册账号')
    LeftClick(read_conf('action80')[0], read_conf('action80')[1])
    time.sleep(1)
    LeftClick(read_conf('action81')[0], read_conf('action81')[1])
    time.sleep(1)
    LeftClick(read_conf('action82')[0], read_conf('action82')[1])
    time.sleep(1)
    for each in username:
        PressOnce(vk_code[each])
        time.sleep(0.1)
    at_code()
    for j in 'qq.com':
        PressOnce(vk_code[j])
        time.sleep(0.1)
    time.sleep(1)

    LeftClick(read_conf('action83')[0], read_conf('action83')[1])
    for pwd in 'chao123456789..':
        time.sleep(0.05)
        PressOnce(vk_code[pwd])
    time.sleep(0.8)

    LeftClick(read_conf('action84')[0], read_conf('action84')[1])
    for pwd in 'chao123456789..':
        time.sleep(0.05)
        PressOnce(vk_code[pwd])
    time.sleep(0.8)
    LeftClick(read_conf('action85')[0], read_conf('action85')[1])
    time.sleep(0.6)
    LeftClick(read_conf('action85.1')[0], read_conf('action85.1')[1])
    time.sleep(0.6)


def cut_server():
    print('切换服务区')
    LeftClick(read_conf('action99')[0], read_conf('action99')[1])
    time.sleep(2)
    LeftClick(read_conf('action100')[0], read_conf('action100')[1])
    time.sleep(3)
    LeftSnap2(670, 711, 675, 666)
    time.sleep(2)
    LeftClick(read_conf('action102')[0], read_conf('action102')[1])
    time.sleep(1)
    LeftClick(read_conf('action103')[0], read_conf('action103')[1])
    time.sleep(2)


def write_conf(content):
    print('账号写入配置')
    new_user = conf.get('user', 'new_user')
    new_user = str(content) + ',' + new_user
    conf.set('user', 'new_user', new_user)
    with open('auto.conf', 'w', encoding='utf-8') as f:
        conf.write(f)


def say(content):
    engine = pyttsx3.init()
    engine.say(content)
    engine.runAndWait()


def agree_join():
    time.sleep(0.5)
    LeftClick(read_conf('action104')[0], read_conf('action104')[1])


def game_play():
    print('选好模式，游戏开始')
    aa = time.time()
    username = conf.get('user', 'username')
    mode = conf.get('mode', 'auto')
    action = conf.get('mode', 'action')
    try:
        user_list = username.split(',')
    except:
        user_list = username
    print(user_list)
    for each in user_list:
        change_user(username=each)
        if mode == 'true':
            time.sleep(8)
            a = '1'
        else:
            a = input('是否下一个账号。。1进入公会申请')
        if a == '1':
            if action == 'exp':
                exp_get()
            elif action == 'donate':
                join_gonghui()
                print('等待你的同意速度！！')
                # say('等待你的同意速度')
                agree_join()
                change_user(username=each)
                # wait for
                time.sleep(7)
                click_gonghui()
                if mode == 'true':
                    time.sleep(3.1415)
                else:
                    b = input('是否下一个账号。。')
            elif action == 'all':
                exp_get()
                time.sleep(3)
                join_gonghui()
                print('等待你的同意速度！！')
                agree_join()
                change_user(username=each)
                # wait for
                time.sleep(7)
                click_gonghui()
                if mode == 'true':
                    time.sleep(3.1415)
                else:
                    b = input('是否下一个账号。。')
        filename = './rules/%s.png' % each
        window_capture(filename=filename)

    bb = time.time()
    print('\n一波用时：%s秒' % (bb - aa))


def game_register():
    print('注册游戏账号')
    for name in range(355209881, 355209882):
        a = time.time()
        # clear_buffer()
        # time.sleep(15)
        register(str(name))
        time.sleep(3)
        cut_server()
        time.sleep(15)
        register(str(name))
        time.sleep(3)
        register_username(username=str(name))
        write_conf(name)
        b = time.time()
        print('\n一波用时：%s秒' % (b - a))


if __name__ == '__main__':
    # game_register()
    game_play()
