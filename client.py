import socket
import sys
import segment
from bitstring import BitArray

if (sys.argv[1] == '-m'):
    HOST = '192.168.0.20'
else:
   HOST = '127.0.0.1'

#HOST = '192.168.43.57'

print("########################")
print("#       CLIENT         #")
print("########################")


PORT = 4666
flag =socket.SHUT_RDWR
num = 666

frame = BitArray(0)
operation = segment.Operator('+')
print(f"Operation: {operation}")
#num1 = segment.Number(12)
num1 = BitArray('0b0000000000101011')
print(f"Num1: {num1.bin}")
#num2 = segment.Number(2)
num2 = BitArray('0b1001010001011001')
print(f"Num2: {num2.bin}")
status = BitArray(2)
id = BitArray(8)
frame.append(operation)
frame.append(num1)
frame.append(num2)


print(f"Frame: {frame.bin}")
# a[0] = 1
# a[1] = 1
# print(a)
# b.append(a)
# print(b)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #s.bind(('', 50666))
    print("Connecting")
    s.connect((HOST, PORT))
    print(f"Connected with: {PORT}")
    s.send(str(frame.bin).encode('utf'))
    data = s.recv(1024)
    s.shutdown(flag)
    #echs.close()
    
print("Recieved", repr(data))    


wait = input("PRESS ENTER TO CONTINUE.")
#wait = input("PRESS ENTER TO CONTINUE.")
#wait = input("PRESS ENTER TO CONTINUE.")
