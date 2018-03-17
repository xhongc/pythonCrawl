from socket import *
ip_port = ('127.0.0.1',8080)
back_log = 5
buffer_size = 1024

tcp_server = socket(AF_INET,SOCK_STREAM)
tcp_server.bind(ip_port)
tcp_server.listen(back_log)

print('Server Is Running Now!')
conn,addr = tcp_server.accept()
print('Double Linked :',conn)
print('Client :',addr)

while True:
    data = conn.recv(buffer_size)
    print('Client MSG',data.decode('utf-8'))
    data = input('>>')
    conn.send(data.encode())
conn.close()
tcp_server.close()