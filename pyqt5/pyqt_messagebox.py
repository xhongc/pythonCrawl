import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 messagebox '
        self.left = 50
        self.top = 50
        self.width = 320
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        buttonReply = QMessageBox.question(self,'pyqt message','Do you think I am the most handsome man? ',QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel,QMessageBox.Yes)
        if buttonReply == QMessageBox.Yes:
            print('you are right')
        if buttonReply ==QMessageBox.No:
            print('no no no')
        if buttonReply == QMessageBox.Cancel:
            print('what do you want?')
        self.show()

'''Overview		
QMessageBox.Cancel	QMessageBox.Ok	QMessageBox.Help
QMessageBox.Open	QMessageBox.Save	QMessageBox.SaveAll
QMessageBox.Discard	QMessageBox.Close	QMessageBox.Apply
QMessageBox.Reset	QMessageBox.Yes	QMessageBox.YesToAll
QMessageBox.No	QMessageBox.NoToAll	QMessageBox.NoButton
QMessageBox.RestoreDefaults	QMessageBox.Abort	QMessageBox.Retry'''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

