print("""
########################
#       SERVER         #
########################""")

import socket

HOST = '127.0.0.1'
#HOST = '192.168.0.20'

PORT = 6666
msg = "Stupid Together"

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))
while True:
    data, addres = s.recvfrom(1024)
    if data:
        print("got data", data)
# d = data[0]
# clientAddr = data[1]
    s.sendto(msg.encode("ascii"), addres)

