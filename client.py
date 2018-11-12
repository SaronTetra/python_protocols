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
    print(f"Recieved status: {idPack.bin[67:69]}")
    if idPack[67:69].int == 1:
        sessionID = idPack[69:77]
        print(f"Session ID: {sessionID}")


#Input for package

    op = input("Operator: ")
    while not (op == '+' or op == '-' or op == '*' or op == '/' or op == 'mod' or
    op == '^' or op == 'nck' or op == '%'):
        print("Wrong operator! Permitted operators: ",
        "+, -,  *, /, mod, ^, nck and %")
        op = input("Operator: ")


    num1 = int(input("First number: "))
    while num1 < - 2147483648 or num1 >2147483647:    
        print("Wrong number! Input integer in range ",
        "from  -2,147,483,648 to 2,147,483,647 ")
        num1 = int(input("First number: "))

    num2 = int(input("Second number: "))
    while num2 < - 2147483648 or num1 >2147483647:    
        print("Wrong number! Input integer in range ",
        "from  -2,147,483,648 to 2,147,483,647 ")
        num2 = int(input("First number: "))

    #Creating package
    pack = BitArray()
    pack = package.pack(op, num1, num2, 0, sessionID)
    print (f"Sending: {pack.bin[0:3]} {pack.bin[3:35]} {pack.bin[35:67]}\
    {pack.bin[67:69]} {pack.bin[69:77]} {pack.bin[77:]}")


#Sending package to server
    s.send(pack.tobytes())


#Recieving result from server
    data = BitArray()
    data.append(s.recv(1024))

    print(f"Result: {data.int}")  

#End connection
    s.shutdown(flag)
    s.close()
    

#wait = input("PRESS ENTER TO CONTINUE.")