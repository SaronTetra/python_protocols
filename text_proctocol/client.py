print("""
########################
#       CLIENT         #
########################""")

import socket
import sys
import segment
from bitstring import BitArray

if (sys.argv[1] == 'm'):
    HOST = '192.168.0.20'
else:
    HOST = '127.0.0.1'

#HOST = '192.168.43.57'

PORT = 4666
send = "PUTElita"

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    #s.bind(('', PORT))
    s.sendto(send.encode('ascii'), (HOST, PORT))
    data = s.recvfrom(1024)
    print(f"Server reply: {data.decode('ascii')}")
    
print("Recieved", repr(data))    

