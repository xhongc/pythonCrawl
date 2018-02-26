from PIL import Image
import os
import time
import configparser
import codecs

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
    return int(string_num.upper(), 16)

def load_action():
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
        action_list = [tuple(action_list[i:i+2]) for i in range(0,len(action_list),2)]
        return action_list

conf = configparser.ConfigParser()
conf.readfp(codecs.open('adb.conf',"r","utf-8-sig"))
def write_conf():
    action_list = load_action()
    count =1
    for each in action_list:
        action = 'action%s'%count
        count += 1
        conf.set('action',action,str(each))
    conf.write(open('adb.conf','w'))

