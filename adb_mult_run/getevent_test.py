from PIL import Image
import os
import time

def scr():
    os.system('adb shell screencap -p /sdcard/autojump1.png')
    os.system('adb pull /sdcard/autojump1.png ')
    img = Image.open('autojump1.png')
    print(img.size)

# a = 1920/1366
# b = 1080/768
# c = (a+b)/2
# x = c *687
# y = c* 404
# print(x,y)

# while 1:
#     os.popen('adb shell input tap 968 568')
#     time.sleep(0.1)
scr()