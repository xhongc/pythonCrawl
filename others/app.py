import cal
import counter
from PyQt5.QtWidgets import QApplication,QDialog
import sys

if __name__ == '__main__':

    app = QApplication(sys.argv)

    Dialog = QDialog()

    ui = counter.Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
