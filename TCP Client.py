#J WENTZEL
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8888)) 


print(s.recv(1024).decode('utf-8'))


list_name = ["a", "b", "c", "d", "e", "Michael", "Tracy", "Sarah"]
for data in list_name:
    s.send(data.encode())
    print(s.recv(1024).decode('utf-8'))
