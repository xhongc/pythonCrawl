from PyQt5 import QtWidgets,QtCore
from video import Ui_Dialog
import sys,time,os
import codecs
import configparser
class Video(QtWidgets.QWidget,Ui_Dialog):

    def __init__(self):
        super(Video, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.video_run)
        self.pushButton_2.clicked.connect(self.video_stop)
        self.pushButton_3.clicked.connect(self.write_conf)

    def video_run(self):
        os.system('adb shell getevent  /dev/input/event1  > w.txt')
    def video_stop(self):
        #sys.exit(1)
        os._exit(1)


    def load_action():
        action_list = []
        with open('w.txt', 'r') as f:
            for each in f.readlines():
                if len(each) > 1 and each.split(' ')[1] == '0035':
                    each = each.split(' ')[2].replace('\n', '')
                    each = hex2dec(each)
                    # print(each)
                    action_list.append(each)
                elif len(each) > 1 and each.split(' ')[1] == '0036':
                    each = each.split(' ')[2].replace('\n', '')
                    each = hex2dec(each)
                    action_list.append(each)
            action_list = [tuple(action_list[i:i + 2]) for i in range(0, len(action_list), 2)]
            return action_list

    def write_conf():
        conf = configparser.ConfigParser()
        conf.readfp(codecs.open('adb.conf', "r", "utf-8-sig"))
        action_list = []

        with open('w.txt', 'r') as f:
            for each in f.readlines():
                if len(each) > 1 and each.split(' ')[1] == '0035':
                    each = each.split(' ')[2].replace('\n', '')
                    each = hex2dec(each)
                    # print(each)
                    action_list.append(each)
                elif len(each) > 1 and each.split(' ')[1] == '0036':
                    each = each.split(' ')[2].replace('\n', '')
                    each = hex2dec(each)
                    action_list.append(each)
            #print(action_list)
            action_list = [tuple(action_list[i:i + 2]) for i in range(0, len(action_list), 2)]
        count = 1
        for each in action_list:
            action = 'action%s' % count
            count += 1
            conf.set('action', action, str(each))
        conf.write(open('adb.conf', 'w'))
if __name__ == '__main__':
    # app = QtWidgets.QApplication(sys.argv)
    # myshow = Video()
    # myshow.show()
    # sys.exit(app.exec_())
    a = Video()
    a.write_conf()