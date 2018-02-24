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
# os.system('adb shell getevent  /dev/input/event1  > 1.txt')
def hex2dec(string_num):
    return str(int(string_num.upper(), 16))

action_list = []
with open ('1.txt','r') as f:
    for each in f.readlines():
        if len(each) > 1 and each.split(' ')[1] == '0035' :
            each = each.split(' ')[2].replace('\n','')
            each = hex2dec(each)
            # print(each)
            action_list.append(each)
        elif len(each) > 1 and each.split(' ')[1] == '0036':
            each = each.split(' ')[2].replace('\n','')
            each = hex2dec(each)
            action_list.append(each)

    print(action_list)