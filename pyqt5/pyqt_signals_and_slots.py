from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
        QVBoxLayout)
import sys

class Dialog(QDialog):
    def slot_method(self):
        print('i am a slot method')

    def __init__(self):
        super(Dialog, self).__init__()

        button = QPushButton('CLICK me OK?')
        button.clicked.connect(run)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(button)

        self.setLayout(mainLayout)
        self.setWindowTitle('i am a title - = -')
def run():
    print('run a little')
if __name__ == '__main__':
    app =  QApplication(sys.argv)
    dialog = Dialog()
    sys.exit(dialog.exec_())