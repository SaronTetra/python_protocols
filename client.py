import socket
import sys
import package
from bitstring import BitArray, BitStream

if (sys.argv[1] == '-m'):
    HOST = '192.168.0.20'
else:
   HOST = '127.0.0.1'

# HOST = '127.0.0.1'

print("""
########################
#       CLIENT         #
########################""")



PORT = 4666
flag =socket.SHUT_RDWR
num = 666


pack = BitArray(0)
pack = package.pack('nck', 6, 2)
print (f"Sending: {pack.bin[0:3]} {pack.bin[3:35]} {pack.bin[35:67]}\
 {pack.bin[67:69]} {pack.bin[69:77]} {pack.bin[77:]}")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #s.bind(('', 50666))

    print("Connecting")
    s.connect((HOST, PORT))
    print(f"Connected with: {PORT}")

    s.send(pack.tobytes())


    data = BitStream()
    data.append(s.recv(1024))

    print(f"Result: {data.int}")  

    s.shutdown(flag)
    s.close()
    
  


#wait = input("PRESS ENTER TO CONTINUE.")

