
import socket
import threading
import time


def tcplink(sock, addr):
    print("[Receive a connection request from {}:{}]".format(addr[0], addr[1]))
   
    a = "Wellcome!"
    sock.send(a.encode())
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.send(('Hello,{}!'.format(data.decode('utf-8')).encode('utf-8')))

    sock.close()
    print("[From {}:{} The connection is closed]".format(addr[0], addr[1]))



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('127.0.0.1', 8888))

s.listen(5)
print("Waiting for the client to connect.....")

while True:
  
    sock, addr = s.accept()
    
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
