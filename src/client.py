import json
import socket
import sys

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ADDR, P = sys.argv[1].split(":")
OPT = int(sys.argv[2])

HOST = ADDR.split("/")[0]
PORT = int(P)
dest = (HOST, PORT)

GET = ADDR[len(HOST):]
if not GET:
	GET = '/'
print(GET)

print('dest:\n', dest)
tcp.connect(dest)

http = "GET "+GET+" HTTP/1.1\nHost: "+HOST+"\nAccept: application/json\nConnection: Close\n\n"
# http = "GET /api/ix/1 HTTP/1.1\nUser-Agent: WebSniffer/1.0 (+http://websniffer.cc/)\nHost: www.peeringdb.com\nAccept: */*\nReferer: https://websniffer.cc/\nConnection: Close"
print(http)

tcp.send(http.encode('latin1'))

resp = tcp.recv(1024).decode('latin1')
txt = ""
while len(resp)>0:
	txt += resp
	resp = tcp.recv(1024).decode('latin1')

tcp.close()

# j = json.loads(txt)
print(txt)
