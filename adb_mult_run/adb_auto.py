import os
import time
from PIL import Image
import pytesseract

# size = os.popen('adb shell wm size').read()
# print(size)
#设置金额
# a = time.time()
def work(money,page):
    os.popen('adb shell input tap 380 1032')
    time.sleep(1.2)
    # 添加理由
    os.popen('adb shell input tap 931 419')
    time.sleep(1)
    cmd_reason = 'adb shell input text ' +'261-'+ str(money) + '-0' +str(page)
    # 输入理由
    os.popen(cmd_reason)
    time.sleep(1.68)
    # 点击输金额
    os.popen('adb shell input tap 272 294')
    time.sleep(1)
    # 输入金额
    cmd_money = 'adb shell input text ' + str(money)
    os.popen(cmd_money)
    time.sleep(1)
    # enter
    os.popen('adb shell input tap 496 637')
    # save
    time.sleep(1)
    os.popen('adb shell input tap 708 1259')
    # quit
    time.sleep(1)
    os.popen('adb shell input tap 398 1262')
def scr():
    os.system('adb shell screencap -p /sdcard/autojump1.png')
    os.system('adb pull /sdcard/autojump1.png ')
    img = Image.open('autojump1.png')
    print(img.size)

def jietu():
    box = (206,429,)

scr()
result = Image.open('autojump1.png')
result = pytesseract.image_to_string(result)
