#! /usr/bin/env python
# -*- encoding: utf-8 -*-
import os,time,sys,datetime
import pythoncom,pyHook,win32api,win32com,win32con,win32clipboard
from PIL import ImageGrab
import picchange
global startTime
startTime = time.time()
print (startTime)
#测试代码----------------------
usersrc = 100
testname = "demo"
stopkey = "End"
ScrnKey = "Home"
swich ="Insert"
#-------------------------------
#正常代码------------------------
# usersrc=str(sys.argv[1])
# testname=str(sys.argv[2])
# stopkey=str(sys.argv[3])
# ScrnKey = str(sys.argv[4])
# swich = str(sys.argv[5]) #normal or match
OperationMode="normal"
#-------------------------------
pvopath='./pvo/'+testname+ '.py'
pvopathopfile='./pvo/'+testname+ '.lt'
pvopathsc='./html/capture/'
#启动由前端界面控制，检验截图按钮为Home，停止录屏工具为End
def onMouseEvent(event):
    # 监听鼠标事件
    global x,y
    x,y=event.Position
    nametime=str(int(round(time.time() * 1000)))
    if event.MessageName=="mouse move":
        endTime = time.time()
        mouse_move(x,y,round(2,2))

        startTime = endTime
    if event.MessageName=="mouse left down":
        endTime = time.time()
        Screen_cap(nametime,x, y,300)
        leftclickeventdown(nametime,x,y,round(2,2))
        startTime = endTime
    if event.MessageName=="mouse left up":
        endTime = time.time()
        leftclickeventup(x,y,round(2,2))
        startTime = endTime
    if event.MessageName=="mouse right down":
        endTime = time.time()
        Screen_cap(nametime,x, y,300)
        rightclickeventdown(nametime,x,y,round(2,2))
        startTime = endTime
    if event.MessageName=="mouse right up":
        endTime = time.time()
        rightclickeventup(x,y,round(2,2))
        startTime = endTime


    # else:
    #     global timecount
    #     timecount=timecount+1
    # 返回 True 以便将事件传给其它处理程序
    # 注意，这儿如果返回 False ，则鼠标事件将被全部拦截
    # 也就是说你的鼠标看起来会僵在那儿，似乎失去响应了
    return True


def onKeyboardEvent(event):
    # 监听键盘事件
    nametime = str(int(round(time.time() * 1000)))
    if event.Key == swich:
        global OperationMode
        if OperationMode=="normal":
            OperationMode="match"
        else:
            OperationMode="normal"
    if event.Key == stopkey:
        alterOpeartion()
        sys.exit()
    if event.Key == ScrnKey:
        endTime = time.time()
        Screen_cap("test"+nametime, x, y,usersrc)
        check(nametime,"test"+nametime)
        startTime = endTime
    elif event.MessageName=="key down" :
        endTime = time.time()
        keyevent(nametime,event.Key,round(2,2))
        startTime = endTime
    elif event.MessageName=="key sys down":
        endTime = time.time()
        keyevent(nametime,event.Key,round(2,2))
        startTime = endTime
    # 同鼠标事件监听函数的返回值
    return True

def mouseOP(optime,optionname, x, y, t,optionnamecn):
    fl = open(pvopathopfile, 'a')
    fl.write("%s,%s,%s,%s,%s,%s" % (optime,optionname, x, y, t,optionnamecn))
    fl.write("\n")
    fl.close()

def mouse_move(x,y,t):
    optime = str(int(round(time.time() * 1000)))
    if OperationMode == "normal":
        mouseOP(optime,"mouse_move", x, y, t, "鼠标移动")
    elif OperationMode == "match":
        pass
    # optime=str(int(round(time.time() * 1000)))
    # fl = open(pvopathopfile, 'a')
    # fl.write("%s,mouse_move,%s,%s,%s,鼠标移动"%(optime,x,y,t))
    # fl.write("\n")
    # fl.close()
def leftclickeventdown(optime,x,y,t):
    if OperationMode=="normal":
        mouseOP(optime,"leftclickdown", x, y, t, "鼠标操作")
    elif OperationMode=="match":
        mouseOP(optime,"leftclickdown", x, y, t, "匹配操作")
    # fl = open(pvopathopfile, 'a')
    # fl.write("%s,leftclickdown,%s,%s,%s,鼠标操作"%(optime,x,y,t))
    # fl.write("\n")
    # fl.close()
def leftclickeventup(x,y,t):
    optime = str(int(round(time.time() * 1000)))
    mouseOP(optime,"leftclickup", x, y, t, "鼠标操作")
    # optime = str(int(round(time.time() * 1000)))
    # fl = open(pvopathopfile, 'a')
    # fl.write("%s,leftclickup,%s,%s,%s,鼠标操作" % (optime, x, y, t))
    # fl.write("\n")
    # fl.close()
def rightclickeventup(x,y,t):
    optime = str(int(round(time.time() * 1000)))
    mouseOP(optime,"rightclickup", x, y, t, "鼠标操作")
    # optime = str(int(round(time.time() * 1000)))
    # fl = open(pvopathopfile, 'a')
    # fl.write("%s,rightclickup,%s,%s,%s,鼠标操作" % (optime, x, y, t))
    # fl.write("\n")
    # fl.close()
def rightclickeventdown(optime,x,y,t):
    if OperationMode == "normal":
        mouseOP(optime,"rightclickdown", x, y, t, "鼠标操作")
    elif OperationMode == "match":
        mouseOP(optime,"rightclickdown", x, y, t, "匹配操作")
    # fl = open(pvopathopfile, 'a')
    # fl.write("%s,rightclickdown,%s,%s,%s,鼠标操作" % (optime, x, y, t))
    # fl.write("\n")
    # fl.close()
def keyevent(optime,key,t):
    fl = open(pvopathopfile, 'a')
    fl.write("%s,inputkey,%s,%s,键盘操作"%(optime,key,t))
    fl.write("\n")
    fl.close()
def check(optime,checkname):
    fl = open(pvopathopfile, 'a')
    fl.write("%s,check,%s,关键位置匹配" % (optime,checkname))
    fl.write("\n")
    fl.close()
def readOpeartion():
    if os.path.isfile(pvopathopfile):
        fl = open(pvopathopfile, 'r')
        Opeartionlist=fl.readlines()
        return Opeartionlist
    else:
        return []

def alterOpeartion():
    beforeOpeartion="" #上一步操作
    beforeOpeartiontime="" #上一步操作最大时间
    beforeOpeartiontimestart="" #上一步操作开始时间
    Opeartionflag1=""   #记录操作名1
    Opeartionflag2=""  #记录操作名2
    beforeOpeartionList=[]#记录操作
    OpeartionLists= readOpeartion()#获取操作数据
    OpeartiontimeList=[]
    if os.path.isfile(pvopathopfile):
        os.remove(pvopathopfile)
    fl = open(pvopathopfile, 'a')
    for Opeartionlist in OpeartionLists:#循环读取操作记录
        Opeartion = Opeartionlist.split(",")
        if Opeartion[1]=="leftclickdown" or Opeartion[1]=="rightclickdown":
            beforeOpeartionList.append(Opeartion) #将操作数据中点击操作记录其属性
        else:
            continue
    for beforeOpeartionOne in beforeOpeartionList:#循环读取点击记录数据
        if beforeOpeartionOne[0]<=beforeOpeartiontime and beforeOpeartionOne[1]==beforeOpeartion:#匹配当操作时间在500毫秒内且操作步骤和前置步骤相同
            beforeOpeartion = ""
            beforeOpeartiontime=beforeOpeartiontimestart
            OpeartiontimeList.append(beforeOpeartiontime)
        else:
            beforeOpeartion = beforeOpeartionOne[1]
            beforeOpeartiontimestart=beforeOpeartionOne[0]
            beforeOpeartiontime = str(int(beforeOpeartionOne[0])+500)
    count=0
    doubleconut=0
    for Opeartionlist in OpeartionLists:
        Opeartion = Opeartionlist.split(",")
        if(len(OpeartiontimeList)>0):
            if Opeartion[0] == OpeartiontimeList[count]:
                doubleconut = 0
                if Opeartion[1] == "leftclickdown":
                    Opeartionflag1 = "leftclickdown"
                    Opeartionflag2 = "leftclickup"
                    Opeartion[1] = "doubleleftclick"
                elif Opeartion[1] == "rightclickdown":
                    Opeartionflag1 = "rightclickdown"
                    Opeartionflag2 = "rightclickup"
                    Opeartion[1] = "doublerightclick"
                if count<len(OpeartiontimeList)-1:
                    count=count+1
                else:
                    count=0
                for i in range(5):
                    fl.write(Opeartion[i] + ",")
                fl.write(Opeartion[5])
            elif doubleconut <3 and int(Opeartion[0]) <= int(beforeOpeartiontime):
                if Opeartion[1] == Opeartionflag1 or Opeartion[1] == Opeartionflag2:
                    doubleconut=doubleconut+1
                    continue
                else:
                    fl.write(Opeartionlist)
            else:
                fl.write(Opeartionlist)
        else:
            fl.write(Opeartionlist)
    fl.close()
    fe = open('./pvo/'+testname+".end", 'a')
    fe.close()


    #插入到新的文件中，提取文件保存路径

def Screen_cap20x10(nametime,x,y):
    if not os.path.isdir(pvopathsc+"20x10"):
        os.mkdir(pvopathsc+"20x10")
    boxs=(x-10,y-5,x+10,y+5)
    pic = ImageGrab.grab(boxs)
    pic.save( pvopathsc+"20x10/"+nametime + ".png")
def Screen_cap30x30(nametime,x,y):
    if not os.path.isdir(pvopathsc+"30x30"):
        os.mkdir(pvopathsc+"30x30")
    boxs=(x-15,y-15,x+15,y+15)
    pic = ImageGrab.grab(boxs)
    pic.save( pvopathsc+"30x30/"+nametime + ".png")
def Screen_cap60x30(nametime,x,y):
    if not os.path.isdir(pvopathsc+"60x30"):
        os.mkdir(pvopathsc+"60x30")
    boxs=(x-30,y-15,x+30,y+15)
    pic = ImageGrab.grab(boxs)
    pic.save( pvopathsc+"60x30/"+nametime + ".png")
def Screen_cap60x60(nametime,x,y):
    if not os.path.isdir(pvopathsc+"60x60"):
        os.mkdir(pvopathsc+"60x60")
    boxs=(x-30,y-30,x+30,y+30)
    pic = ImageGrab.grab(boxs)
    pic.save( pvopathsc+"60x60/"+nametime + ".png")
def Screen_cap120x60(nametime,x,y):
    if not os.path.isdir(pvopathsc+"120x60"):
        os.mkdir(pvopathsc+"120x60")
    boxs=(x-60,y-30,x+60,y+30)
    pic = ImageGrab.grab(boxs)
    pic.save( pvopathsc+"120x60/"+nametime + ".png")
def Screen_capUser(nametime,usersrc,x,y):
    if not os.path.isdir(pvopathsc+"User"):
        os.mkdir(pvopathsc+"User")
    if not os.path.isdir(pvopathsc+"source"):
        os.mkdir(pvopathsc + "source")
    if not os.path.isdir(pvopathsc+"target"):
        os.mkdir(pvopathsc + "target")
    usersrc=int(usersrc)
    boxs=(x-usersrc/2,y-usersrc/2,x+usersrc/2,y+usersrc/2)
    pic = ImageGrab.grab(boxs)
    pic.save( pvopathsc+"User/"+nametime + ".png")
def Screen_cap(nametime,x,y,usersrc):
    print(nametime,x,y,usersrc)
    if not os.path.isdir(pvopathsc):
        os.mkdir(pvopathsc)
    Screen_cap30x30(nametime,x,y)
    Screen_cap20x10(nametime,x,y)
    Screen_cap60x30(nametime,x,y)
    Screen_cap60x60(nametime,x,y)
    Screen_cap120x60(nametime,x,y)
    Screen_capUser(nametime,usersrc, x, y)
def main():
    time.sleep(0.5)
    # if not os.path.isfile("./pvo/"+ "html" + '.py'):

    if os.path.isfile("./pvo/"+ testname + '.py'):
        os.remove("./pvo/"+ testname + '.py')
    if os.path.isfile(pvopathopfile,):
        os.remove(pvopathopfile,)
        fl = open(pvopathopfile, 'a')
        fl.close()
    if not os.path.isdir("./pvo"):
        os.mkdir("./pvo")
    if not os.path.isdir("./html"):
        os.mkdir("./html")
    if not os.path.isdir(pvopathsc):
        os.mkdir(pvopathsc)
    # creatfile()
    time.sleep(2)

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
    pythoncom.PumpMessages()

if __name__ == "__main__":
    main()