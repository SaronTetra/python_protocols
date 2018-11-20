import socket
import sys
import package
from bitstring import BitArray, BitStream


# System argv for ip selection
# if (sys.argv[1] == '-m'):
#     HOST = '192.168.0.20'
# else:
#    HOST = '127.0.0.1'
HOST = '127.0.0.1'
#HOST = '192.168.0.20'

#Connection variables
PORT = 4666
flag =socket.SHUT_RDWR


print("""
########################
#       CLIENT         #
########################""")


#Creating socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #s.bind(('', 50666))

#Connecting to server
    print("Connecting")
    s.connect((HOST, PORT))
    print(f"Connected with: {PORT}")


#Recieve ID
    idPack = BitArray(0)
    sessionID = BitArray()
    idPack.append(s.recv(1024))
    print(f"Recieved status: {idPack.bin[35:37]}")
    # if idPack.bin[35:37] == 1:
    sessionID = idPack[37:45]
    print(f"Session ID: {sessionID}")


#Input for package
    #print(f"CLIENT ID")
    package.sendFirst(sessionID, s, 0)
    package.sendPackage(sessionID, s)



#End connection
    s.shutdown(flag)
    s.close()
    

#wait = input("PRESS ENTER TO CONTINUE.") socket.AF_INET, socket.SOCK_STREAM