import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class APP(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'pyqt_button'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        button = QPushButton('Pyqt button',self)
        button.setToolTip('Do or not to do ')
        button.move(100,70)
        button.clicked.connect(self.on_click)

        self.show()
    @pyqtSlot()
    def on_click(self):
        print('successful job')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = APP()
    sys.exit(app.exec_())