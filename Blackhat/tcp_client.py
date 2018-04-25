import socket
from pprint import pprint
target_host = '127.0.0.1'
target_port = 9999

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((target_host,target_port))
client.send(b'GET / HTTP/1.1\r\nHost:baidu.com\r\n\r\n')
response = client.recv(4096)
pprint(response)