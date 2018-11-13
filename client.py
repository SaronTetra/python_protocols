import socket
import sys
import package
from bitstring import BitArray, BitStream


#System argv for ip selection
# if (sys.argv[1] == '-m'):
#     HOST = '192.168.0.20'
# else:
#    HOST = '127.0.0.1'
HOST = '127.0.0.1'


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
    print(f"Recieved status: {idPack.bin[45:]}")
    if idPack[45:].int == 1:
        sessionID = idPack[37:45]
        print(f"Session ID: {sessionID}")


#Input for package

    quantity = input("Do you want to calculate on more than two numbers? (y/n) ")
    while not (quantity == 'y' or quantity == 'n'):
        print("Wrong answer! Permitted answers: ",
        "y and n")


    if quantity == 'n':
        package.sendTwo(sessionID, s, 1)
    elif quantity == 'y':
        package.sendTwo(sessionID, s, 0)
        package.sendOne(sessionID, s)


#Recieving result from server
    # data = BitArray()
    # data.append(s.recv(1024))

    # print(f"Result: {data.int}")  

#End connection
    s.shutdown(flag)
    s.close()
    

#wait = input("PRESS ENTER TO CONTINUE.")