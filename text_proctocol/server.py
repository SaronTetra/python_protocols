print("""
########################
#       SERVER         #
########################""")

import socket

HOST = '127.0.0.1'
#HOST = '192.168.43.102'
#HOST = '192.168.0.21'

PORT = 6666
msg = "Stupid Together"

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    data = s.recvfrom(1024)
    d = data[0]
    clientAddr = data[1]
    s.sendto(msg, clientAddr)

