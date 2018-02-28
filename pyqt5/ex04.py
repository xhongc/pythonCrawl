from PyQt5 import QtWidgets,QtCore
from button import Ui_Dialog
import sys,time
import configParser

class Mysign(QtWidgets.QWidget,Ui_Dialog):
    _signal = QtCore.pyqtSignal(str) # 定义信号

    def __init__(self):
        super(Mysign, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.prn)
        self._signal.connect(self.mysignalslot)
    def prn(self):
        print('test')
        time.sleep(1)
        print('sleep 1s')
        self._signal.emit('你是槽') #发射信号
    def mysignalslot(self,param):
        print('wo shi cao !',param)
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myshow = Mysign()
    myshow.show()
    sys.exit(app.exec_())