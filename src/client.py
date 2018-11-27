import json
import socket
import sys

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print (sys.argv[1])
ADDR = sys.argv[1].split(":")
OPT = int(sys.argv[2])

HOST = ADDR[0]
PORT = int(ADDR[1])
dest = (HOST, PORT)

msg = "GET / HTTP/1.1\n"+HOST+"\n\n"

tcp.connect(dest)

tcp.sendall (msg.encode('latin1'))

resp = tcp.recv(1024)#.decode('latin1')

print(resp)

tcp.close()
