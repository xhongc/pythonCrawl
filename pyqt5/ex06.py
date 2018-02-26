from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QMainWindow,QMessageBox
from menu import Ui_MainWindow
import sys,time
class Mainwindows(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(Mainwindows, self).__init__()
        self.setupUi(self)
        self.action111.triggered.connect(self.openmsg)

    def openmsg(self):
        print('open open open op')
        res = QMessageBox.information(self,'open','you click on button',
                                      QMessageBox.StandardButtons(QMessageBox.Yes|QMessageBox.No))
        self.statusBar().showMessage('sure open this')


if __name__ == '__main__':
    app =  QtWidgets.QApplication(sys.argv)
    myshow = Mainwindows()
    myshow.show()
    sys.exit(app.exec_())