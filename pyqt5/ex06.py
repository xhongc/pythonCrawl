from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QMainWindow,QMessageBox,QGridLayout
from menu import Ui_MainWindow
from children import Ui_children
import sys,time
class children(QtWidgets.QWidget,Ui_children):
    def __init__(self):
        super(children, self).__init__()
        self.setupUi(self)
class Mainwindows(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(Mainwindows, self).__init__()
        self.setupUi(self)
        #self.action111.triggered.connect(self.openmsg)
        self.child = children()
        self.QGridLayout.addWidget(self.child)

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