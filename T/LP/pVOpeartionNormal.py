#! /usr/bin/env python
# -*- encoding: utf-8 -*-
import win32gui, win32ui, win32con, win32api
import win32clipboard as wc
import sys, time, os
from PIL import Image as img
from PIL import ImageGrab

from ImageRecognize import ImageRecognize
from AR_User.cof.im import SendNew99U
from ctypes import *
from htmldemo import *

#--------------------------------------键盘码-------------------------------------
VK_CODE = {
    'Back'                  : 0x08, 'Tab': 0x09, 'clear': 0x0C, 'Return': 0x0D, 'shift': 0x10, 'ctrl': 0x11,
    'alt'                   : 0x12, 'Pause': 0x13, 'Capital': 0x14, 'Escape': 0x1B, 'Space': 0x20, 'Prior': 0x21,
    'Next'                  : 0x22, 'End': 0x23, 'Home': 0x24, 'Left': 0x25,
    'Up'                    : 0x26, 'Right': 0x27, 'Down': 0x28, 'select': 0x29, 'Snapshot': 0x2A, 'execute': 0x2B,
    'print_screen'          : 0x2C, 'Insert': 0x2D, 'Delete': 0x2E, 'help': 0x2F, '0': 0x30, '1': 0x31, '2': 0x32,
    '3'                     : 0x33, '4': 0x34, '5': 0x35, '6': 0x36,
    '7'                     : 0x37, '8': 0x38, '9': 0x39, 'A': 0x41, 'B': 0x42, 'C': 0x43, 'D': 0x44, 'E': 0x45,
    'F'                     : 0x46, 'G': 0x47, 'H': 0x48, 'I': 0x49, 'J': 0x4A, 'K': 0x4B, 'L': 0x4C, 'M': 0x4D,
    'N'                     : 0x4E, 'O': 0x4F, 'P': 0x50, 'Q': 0x51, 'R': 0x52, 'S': 0x53, 'T': 0x54, 'U': 0x55,
    'V'                     : 0x56, 'W': 0x57, 'X': 0x58, 'Y': 0x59, 'Z': 0x5A, 'Numpad0': 0x60, 'Numpad1': 0x61,
    'Numpad2'               : 0x62, 'Numpad3': 0x63, 'Numpad4': 0x64, 'Numpad5': 0x65, 'Numpad6': 0x66, 'Numpad7': 0x67,
    'Numpad8'               : 0x68, 'Numpad9': 0x69, 'Multiply': 0x6A,
    'Add'                   : 0x6B, 'Subtract': 0x6D, 'Decimal': 0x6E, 'Divide': 0x6F, 'F1': 0x70, 'F2': 0x71,
    'F3'                    : 0x72, 'F4': 0x73, 'F5': 0x74, 'F6': 0x75, 'F7': 0x76, 'F8': 0x77, 'F9': 0x78, 'F10': 0x79,
    'F11'                   : 0x7A, 'F12': 0x7B,
    'F13'                   : 0x7C, 'F14': 0x7D, 'F15': 0x7E, 'F16': 0x7F, 'F17': 0x80, 'F18': 0x81, 'F19': 0x82,
    'F20'                   : 0x83, 'F21': 0x84, 'F22': 0x85, 'F23': 0x86, 'F24': 0x87, 'Numlock': 0x90, 'Scroll': 0x91,
    'Lshift'                : 0xA0, 'Rshift ': 0xA1,
    'Lcontrol'              : 0xA2, 'Rcontrol': 0xA3, 'Lmenu': 0xA4, 'Rmenu': 0xA5, 'browser_back': 0xA6,
    'browser_forward'       : 0xA7, 'browser_refresh': 0xA8, 'browser_stop': 0xA9, 'browser_search': 0xAA,
    'browser_favorites'     : 0xAB,
    'browser_start_and_home': 0xAC, 'volume_mute': 0xAD, 'volume_Down': 0xAE, 'volume_up': 0xAF, 'next_track': 0xB0,
    'previous_track'        : 0xB1, 'stop_media': 0xB2, 'play/pause_media': 0xB3, 'start_mail': 0xB4,
    'select_media'          : 0xB5,
    'start_application_1'   : 0xB6, 'start_application_2': 0xB7, 'attn_key': 0xF6, 'crsel_key': 0xF7, 'exsel_key': 0xF8,
    'play_key'              : 0xFA, 'zoom_key': 0xFB, 'clear_key': 0xFE, 'Oem_Plus': 0xBB, 'Oem_Comma': 0xBC, 'Oem_Minus': 0xBD, 'Oem_Period': 0xBE,
    'Oem_2'                     : 0xBF, 'Oem_3': 0xC0,
    'Oem_1'                     : 0xBA, 'Oem_4': 0xDB, 'Oem_5': 0xDC, 'Oem_6': 0xDD, "Oem_7": 0xDE}
#--------------------------------------操作指令-------------------------------------
MOUSEEVENTF_MOVE = 0x0001  # mouse move.
MOUSEEVENTF_ABSOLUTE = 0x8000  # absolute move
MOUSEEVENTF_MOVEABS = MOUSEEVENTF_MOVE + MOUSEEVENTF_ABSOLUTE
MOUSEEVENTF_LEFTDOWN = 0x0002  # left button down
MOUSEEVENTF_LEFTUP = 0x0004  # left button up
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_CLICK = MOUSEEVENTF_LEFTDOWN + MOUSEEVENTF_LEFTUP
reload(sys)
sys.setdefaultencoding('UTF-8')  # 将脚本编码格式转化为指定的编码格式
displayX=win32api.GetSystemMetrics(0)
displayY=win32api.GetSystemMetrics(1)

class pVOpeartion(object):
    def __init__(self,testID,checknum,jj):
        self.jj=jj
        self.testID=str(testID)
        self.checknum=str(checknum)
        if os.path.isfile("./LP/pvo/" +self.testID + ".match"):
            os.remove("./LP/pvo/" +self.testID + ".match")
        self.testDO()
        htmldemo(self.testID)
        fo = open("./LP/pvo/" +  self.testID + ".over", 'a')
        fo.close()

    def window_capture(self, testname):
        pic = ImageGrab.grab()
        pic.save(r"./LP/html/capture/source/%s.png" % testname)

    def timeImageName(self):
        return time.strftime("%Y%m%d%H%M%S", time.localtime())

    def imgPair(self, pngModelName, x=displayX, y=displayY, Accurate=0.8):
        print ("imgPair", displayX, displayY)
        self.imgTimename = self.timeImageName()
        self.window_capture(self.imgTimename)
        imgdict = ImageRecognize.proxy(r"./LP/html/capture/User/%s.png" % pngModelName,
                                       r"./LP/html/capture/source/%s.png" % self.imgTimename,
                                       r"./LP/html/capture/target/%s.png" % self.imgTimename, srcX=x, srcY=y,defaultAccurate=Accurate)
        if imgdict["match"]:
            fmatch = open("./LP/pvo/" +self.testID+ ".match", 'a')
            fmatch.write(u"%s,%s,%s,匹配" % (self.imgTimename, pngModelName, self.imgTimename))
            fmatch.close()
        else:
            fmatch = open("./LP/pvo/" +self.testID+ ".match", 'a')
            fmatch.write(u"%s,%s,%s,未匹配" % (self.imgTimename, pngModelName, self.imgTimename))
            fmatch.close()
        return imgdict["match"], imgdict["maxLocX"], imgdict["maxLocY"], self.imgTimename

    def imgPairOP(self, pngModelName, x=displayX, y=displayY, Accurate=0.8):
        print ("imgPairOP", displayX, displayY)
        self.imgTimename = self.timeImageName()
        self.window_capture(self.imgTimename)
        imgdict = ImageRecognize.proxy(r"./LP/html/capture/User/%s.png" % pngModelName,
                                       r"./LP/html/capture/source/%s.png" % self.imgTimename,
                                       r"./LP/html/capture/target/%s.png" % self.imgTimename, srcX=x, srcY=y,defaultAccurate=Accurate)
        return imgdict["match"], imgdict["maxLocX"], imgdict["maxLocY"]
    def imgpairLclick(self, pngModelName):
        match, x, y = self.imgPairOP(pngModelName)
        if match:
            self.leftclickdown(x, y, 0.2)
        time.sleep(1)
    def imgpairDLclick(self, pngModelName):
        match, x, y = self.imgPairOP(pngModelName)
        if match:
            self.doubleleftclick(x, y, 0.2)
        time.sleep(1)

    def imgpairDRclick(self, pngModelName):
        match, x, y = self.imgPairOP(pngModelName)
        if match:
            self.doublerightclick(x, y, 0.2)
        time.sleep(1)

    def imgpairRclick(self, pngModelName):
        match, x, y = self.imgPairOP(pngModelName)
        if match:
            self.rightclickdown(x, y, 0.2)
        time.sleep(1)
    def mouse_move(self, x, y, t=0.6):
        windll.user32.SetCursorPos(x, y)
        time.sleep(t)

    def leftclickdown(self, x, y, t):
        if not x is None and not y is None:
            self.mouse_move(x, y)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(t)

    def leftclickup(self, x, y, t):
        if not x is None and not y is None:
            self.mouse_move(x, y)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        time.sleep(t)

    def doubleleftclick(self, x, y, t):
        if not x is None and not y is None:
            self.mouse_move(x, y)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        time.sleep(t)

    def rightclickdown(self, x, y, t):
        if not x is None and not y is None:
            self.mouse_move(x, y)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        time.sleep(t)

    def rightclickup(self, x, y, t):
        if not x is None and not y is None:
            self.mouse_move(x, y)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        time.sleep(t)

    def doublerightclick(self, x, y, t):
        if not x is None and not y is None:
            self.mouse_move(x, y)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        time.sleep(t)

    def inputkey(self, str, t):
        win32api.keybd_event(VK_CODE[str], 0, 0, 0)
        win32api.keybd_event(VK_CODE[str], 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(t)

    def send99U(self, content):
        group_list = [self.jj]
        send_o = SendNew99U()
        send_o.send_to_receivers(content, group_list)

    def check(self, checkname):
        match, x, y, imgTimename = self.imgPair(checkname)
        return match, imgTimename


    def readOpeartion(self):
        fl = open("./LP/pvo/" +self.testID+ ".lt", 'r')
        Opeartionlistnum = fl.readlines()
        return Opeartionlistnum

    def testDO(self):
        global starttime,rightcount,count
        starttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        rightcount = 0
        count = 0
        for Opeartion in self.readOpeartion():
            Opeartionlist = Opeartion.split(",")
            if len(Opeartionlist)==6:
                Opeartionlist[5]=Opeartionlist[5].strip()
            if Opeartionlist[1] == "inputkey":
                eval("self." + Opeartionlist[1] + "('" + Opeartionlist[2] + "'," + Opeartionlist[3] + ")")
            elif (Opeartionlist[1] == "check"):
                match, imgTimename = eval("self.check('test'+Opeartionlist[0])")
                if match:
                    count = count + 1.0
                    rightcount = rightcount + 1.0
                    count = count + 1.0
            elif Opeartionlist[5]=="鼠标操作" or Opeartionlist[5]=="鼠标移动" :
                eval("self." + Opeartionlist[1] + "(" + Opeartionlist[2] + "," + Opeartionlist[3] + "," + Opeartionlist[4] + ")")
            elif Opeartionlist[5] == "匹配操作":
                if '\xef\xbb\xbf' in Opeartionlist[0]:
                    str1 = Opeartionlist[0].replace('\xef\xbb\xbf', '')  # 用replace替换掉'\xef\xbb\xbf'
                    Opeartionlist[0]=int(str1.strip()) # strip()去掉\n
                else:
                    Opeartionlist[0]=int(Opeartionlist[0].strip())
                if (Opeartionlist[1] == "leftclickdown"):
                    eval("self.imgpairLclick(\"" + str(Opeartionlist[0])+ "\")")
                elif (Opeartionlist[1] == "rightclickdown"):
                    eval("self.imgpairRclick(\"" + str(Opeartionlist[0])+ "\")")
                elif (Opeartionlist[1] == "doubleleftclick"):
                    eval("self.imgpairDLclick(\"" + str(Opeartionlist[0]) + "\")")
                elif (Opeartionlist[1] == "doublerightclick"):
                    eval("self.imgpairDRclick(\"" + str(Opeartionlist[0])+ "\")")


        endtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        if count != 0:
            checknum = rightcount / count
            if checknum >= float(self.checknum):
                fdata = open("./LP/pvo/" +self.testID+ ".result", 'a')
                fdata.write(self.testID.decode("GBK") + ";%s;%s;%s;通过;%s;limegreen;" % (
                starttime, endtime, count, str(checknum * 100)))
                fdata.close()
                self.send99U(self.testID.decode("GBK") + "关键点测试%s个;达到测试标准;通过，测试概率为%s" % (
                count, str(checknum * 100)))
            else:
                fdata = open("./LP/pvo/" +self.testID+ ".result", 'a')
                fdata.write(self.testID.decode("GBK") + ";%s;%s;%s;不通过;%s;indianred;" % (
                starttime, endtime, count, str(checknum * 100)))
                fdata.close()
                self.send99U(self.testID.decode("GBK") + "关键点测试%s个;未达到测试标准;不通过，测试概率为%s" % (
                count, str(checknum * 100)))


if "__main__"==__name__:
    pVOpeartion(sys.argv[1],float(sys.argv[2])*0.01,sys.argv[3])
    # pVOpeartion("z20171120112239",float(75)*0.01,150915)
