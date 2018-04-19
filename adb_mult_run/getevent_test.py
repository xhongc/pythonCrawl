from PIL import Image
import os
import time
import configparser
import codecs
from PIL import ImageGrab,ImageChops

def video():
    os.system('adb shell getevent  /dev/input/event1  > 1.txt')

def scr(action):
    if not os.path.exists("cature/60x30"):
        os.makedirs("cature/60x30")

    os.system('adb shell screencap -p /sdcard/autojump1.png')
    os.system('adb pull /sdcard/autojump1.png ')
    img = Image.open('autojump1.png')

    # print(img.size)
    x,y = read_conf(action)[0],read_conf(action)[1]

    box = (x-100,y-15,x+100,y+15)
    pic = img.crop(box)
    pic.save("cature/60x30/" + action + ".png")

def judge_pic(now,action):
    if not os.path.exists("now/60x30"):
        os.makedirs("now/60x30")

    os.system('adb shell screencap -p /sdcard/autojump1.png')
    os.system('adb pull /sdcard/autojump1.png ')
    img = Image.open('autojump1.png')

    # print(img.size)
    x,y = read_conf(action)[0],read_conf(action)[1]

    box = (x-100,y-15,x+100,y+15)
    pic = img.crop(box)
    pic.save("now/60x30/" + now + ".png")

    image1 = Image.open('now/60x30/%s.png' % (now))
    image2 = Image.open('cature/60x30/%s.png' % (action))
    im = ImageChops.difference(image1, image2).getbbox()
    print(im)
    return im

def scr_and_diff(now,action):
    im = judge_pic(now,action)
    #print(im)
    im_count = 1
    while im:
        time.sleep(0.2)
        #print(im)
        im = judge_pic(now,action)
        im_count += 1

        if im_count == 20:
            im_text = u'出现未知错误！'
            im_a = input(im_text)
    return im
# a = 1920/1366
# b = 1080/768
# c = (a+b)/2
# x = c *687
# y = c* 404
# print(x,y)

# while 1:
#     os.popen('adb shell input tap 968 568')
#     time.sleep(0.1)

#
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

def read_conf(action):
    action_conf =conf.get('action',action)
    action_conf = action_conf.replace('(','').replace(')','').replace(' ','').split(',')
    return int(action_conf[0]),int(action_conf[1])

def work_once(money,page):
    id = conf.get('set','id')
    scr('action1')
    os.popen('adb shell input tap %s %s'%(read_conf('action1')[0],read_conf('action1')[1]))
    time.sleep(2)

    scr('action2')
    os.popen('adb shell input tap %s %s' % (read_conf('action2')[0], read_conf('action2')[1]))
    time.sleep(0.5)
    reason = id + '-' + str(money) + '-0' + str(page)
    os.popen('adb shell input text %s'%reason)
    time.sleep(0.5)
    # os.popen('adb shell input tap %s %s' % (read_conf('action3')[0], read_conf('action3')[1]))
    # scr('action3')
    # time.sleep(0.2)
    # os.popen('adb shell input tap %s %s' % (read_conf('action4')[0], read_conf('action4')[1]))
    # scr('action4')
    # time.sleep(0.2)
    os.popen('adb shell input tap %s %s' % (read_conf('action5')[0], read_conf('action5')[1]))
    #scr('action5')
    time.sleep(0.5)
    # os.popen('adb shell input tap %s %s' % (read_conf('action6')[0], read_conf('action6')[1]))
    # scr('action6')
    # time.sleep(0.2)
    os.popen('adb shell input text %s' % str(money))
    time.sleep(0.5)

    scr('action7')
    os.popen('adb shell input tap %s %s' % (read_conf('action7')[0], read_conf('action7')[1]))
    time.sleep(2)

    scr('action8')
    os.popen('adb shell input tap %s %s' % (read_conf('action8')[0], read_conf('action8')[1]))

    time.sleep(2)
    os.popen('adb shell input tap %s %s' % (read_conf('action9')[0], read_conf('action9')[1]))
    #scr('action9')
    time.sleep(2)

def work(money,page):
    id = conf.get('set', 'id')
    scr_and_diff('now1', 'action1')
    os.popen('adb shell input tap %s %s' % (read_conf('action1')[0], read_conf('action1')[1]))

    time.sleep(1)
    scr_and_diff('now2', 'action2')
    os.popen('adb shell input tap %s %s' % (read_conf('action2')[0], read_conf('action2')[1]))

    time.sleep(0.5)
    reason = id + '-' + str(money) + '-0' + str(page)
    os.popen('adb shell input text %s' % reason)
    time.sleep(0.5)

    #scr_and_diff('now5', 'action5')
    os.popen('adb shell input tap %s %s' % (read_conf('action5')[0], read_conf('action5')[1]))

    time.sleep(0.2)
    os.popen('adb shell input text %s' % str(money))

    time.sleep(0.5)
    scr_and_diff('now7', 'action7')
    os.popen('adb shell input tap %s %s' % (read_conf('action7')[0], read_conf('action7')[1]))

    time.sleep(0.2)
    scr_and_diff('now8', 'action8')
    os.popen('adb shell input tap %s %s' % (read_conf('action8')[0], read_conf('action8')[1]))

    time.sleep(0.2)
    # scr_and_diff('now9', 'action9')
    os.popen('adb shell input tap %s %s' % (read_conf('action9')[0], read_conf('action9')[1]))

if __name__ == '__main__':
    video()
    #write_conf()
    # a = time.time()
    # work(1,1)
    # b = time.time()
    # print(b-a)
    #work_once(1,1)
    #scr_and_diff('now2', 'action2')

