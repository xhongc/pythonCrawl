import socket

phone = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
phone.bind(('127.0.0.1',8080))
phone.listen(5)
print('-------------->')
conn,addr = phone.accept()

msg = conn.recv(1024)
print('客户端发来消息是：',msg)
conn.send(msg.upper())

conn.close()
phone.close()