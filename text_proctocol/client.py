print("""
########################
#       CLIENT         #
########################""")

import socket
import sys

# if (sys.argv[1] == 'm'):
#     HOST = '192.168.0.20'
# else:
HOST = '127.0.0.1'

PORT = 6666
send = "PUTElita"

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(send.encode('ascii'), (HOST, PORT))
data, server = s.recvfrom(1024)
print(f"Server reply: {data}")
    
print("Recieved", repr(data))
s.close()


