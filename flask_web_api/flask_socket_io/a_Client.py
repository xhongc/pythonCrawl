import socket

phone = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
phone.connect(('127.0.0.1',8080))

phone.send('hello chao'.encode('utf-8'))
data = phone.recv(1024)
print('受大盘服务端的信息 ',data)
phone.close()