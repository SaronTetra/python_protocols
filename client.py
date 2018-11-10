import socket
import sys
import package
from bitstring import BitArray, BitStream


#System argv for ip selection
if (sys.argv[1] == '-m'):
    HOST = '192.168.0.20'
else:
   HOST = '127.0.0.1'


#Connection variables
PORT = 4666
flag =socket.SHUT_RDWR


print("""
########################
#       CLIENT         #
########################""")

#Input for package TODO: check if input is right(try, catch), check range
op = input("Operation: ")
num1 = int(input("First number: "))
num2 = int(input("Second number: "))


sessionID = package.IDGen()

#Creating package
pack = BitArray(0)
pack = package.pack(op, num1, num2)
print (f"Sending: {pack.bin[0:3]} {pack.bin[3:35]} {pack.bin[35:67]}\
 {pack.bin[67:69]} {pack.bin[69:77]} {pack.bin[77:]}")
#too much padding, why?

#Creating socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #s.bind(('', 50666))

#Connecting to server
    print("Connecting")
    s.connect((HOST, PORT))
    print(f"Connected with: {PORT}")


#Sending package to server
    s.send(pack.tobytes())


#Recieving result from server
    data = BitStream()
    data.append(s.recv(1024))

    print(f"Result: {data.int}")  

#End connection
    s.shutdown(flag)
    s.close()
    

#wait = input("PRESS ENTER TO CONTINUE.")