from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QMessageBox,QInputDialog,QLineEdit,QFileDialog
from button import Ui_Dialog
import sys,time

class Mysign(QtWidgets.QWidget,Ui_Dialog):
    _signal = QtCore.pyqtSignal(str) # 定义信号

    def __init__(self):
        super(Mysign, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.msg3)
        self._signal.connect(self.mysignalslot)
    def prn(self):
        print('test')
        time.sleep(1)
        print('sleep 1s')
        self._signal.emit('你是槽') #发射信号
    def mysignalslot(self,param):
        print('wo shi cao !',param)
    def msg(self):
        ok = QMessageBox.information(self,'this is titile','this is info',
                                     QMessageBox.StandardButtons(QMessageBox.Yes|QMessageBox.No))

    def msg1(self):
        result,ok = QInputDialog.getText(self,'input here','Tip',QLineEdit.Password,'DEFOULT')
        print(result,ok)
    def msg2(self):
        item = ['hello','hi','ho']
        result, ok = QInputDialog.getItem(self, 'input here', 'Tip',item,1,True) # 1 为默认选中项目  True/False列表框是否可编辑
        print(result, ok)
    def msg3(self):
        filename,select = QFileDialog.getOpenFileName(
            self,'Title','D:\work\Python\pythonCrawl\pyqt5','程序过滤(*.exe)',None
        )
        print(filename,select)
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myshow = Mysign()
    myshow.show()
    sys.exit(app.exec_())