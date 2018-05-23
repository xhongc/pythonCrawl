# import cal
# import counter
# from PyQt5.QtWidgets import QApplication,QDialog
# import sys
#
# if __name__ == '__main__':
#
#     app = QApplication(sys.argv)
#
#     Dialog = QDialog()
#
#     ui = counter.Ui_Dialog()
#     ui.setupUi(Dialog)
#     Dialog.show()
#     sys.exit(app.exec_())
b = b"Hello, world!"  # bytes object
s = "Hello, world!"   # str object

print('str --> bytes')
print(bytes(s, encoding="utf8"))
print(str.encode(s))   # 默认 encoding="utf-8"
print(s.encode())      # 默认 encoding="utf-8"

print('\nbytes --> str')
print(str(b, encoding="utf-8"))
print(bytes.decode(b))  # 默认 encoding="utf-8"
print(b.decode())       # 默认 encoding="utf-8"