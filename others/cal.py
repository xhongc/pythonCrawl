from PyQt5 import QtWidgets
from counter import Ui_Dialog
import sys, time, os
import codecs
import os


class Video(QtWidgets.QWidget, Ui_Dialog):
    def __init__(self):
        super(Video, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.on_click_1)
        self.pushButton_2.clicked.connect(self.on_click_2)
        self.pushButton_3.clicked.connect(self.on_click_3)
        self.pushButton_4.clicked.connect(self.on_click_6)
        self.pushButton_5.clicked.connect(self.on_click_4)
        self.pushButton_6.clicked.connect(self.on_click_5)
        # self.pushButton_7.clicked.connect(self.on_click_9)
        self.pushButton_8.clicked.connect(self.on_click_8)
        self.pushButton_9.clicked.connect(self.on_click_7)
        self.pushButton_10.clicked.connect(self.on_click_jian)

        self.pushButton_15.clicked.connect(self.on_click_deng)
        self.pools = []

    def on_click_1(self):
        tmp = '1'
        self.pools.append(tmp)

    def on_click_2(self):
        tmp = '2'
        self.pools.append(tmp)

    def on_click_3(self):
        tmp = '3'
        self.pools.append(tmp)

    def on_click_4(self):
        tmp = '6'
        self.pools.append(tmp)

    def on_click_5(self):
        tmp = '4'
        self.pools.append(tmp)

    def on_click_6(self):
        tmp = '5'
        self.pools.append(tmp)

    def on_click_7(self):
        tmp = '9'
        self.pools.append(tmp)

    def on_click_8(self):
        tmp = '8'
        self.pools.append(tmp)

    def on_click_jian(self):
        tmp = '-'
        self.pools.append(tmp)

    def on_click_deng(self):
        if '-' in self.pools:
            index_jian = self.pools.index('-')
            a = ''.join(self.pools[:index_jian])
            b = ''.join(self.pools[index_jian+1:])
            result = int(a) - int(b)
            print(result)
        #self.lineEdit.setText(result)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myshow = Video()
    myshow.show()
    sys.exit(app.exec_())
