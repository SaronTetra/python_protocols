import socket
import package
from bitstring import BitArray, BitStream

print("""
########################
#       SERVER         #
########################""")

HOST = '127.0.0.1'
HOST = '192.168.0.20'

PORT = 4666

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))

    print("Listening")
    s.listen()
    conn, addr = s.accept()

    with conn:
        print("Connected by", addr)
        while True:
            data = BitStream()
            data.append(conn.recv(1024))
            if not data:
                break

            print(f"Recieved: {data.bin[0:3]} {data.bin[3:35]} {data.bin[35:67]}\
             {data.bin[67:69]} {data.bin[69:77]} {data.bin[77:]}")
            print(f"Recieved: ", data.bin)
            #strings = str(data.decode('utf'))
            #print(f"decode: {strings}")
            

            operation = data[0:3].bin #czyta bajty, nie bity
            #num1 = BitArray(32)
            #num2 = BitArray(32)
            a = data[3:35].int
            b = data[35:67].int
            print(f"A: {a}, B:{b}")
            status = data[67:69]
            id = data[69:77]
            

            # while x != 'q':
            # x = input("Commands pls ")
            print("Operation: " + str(operation))
            result = package.countTwo(operation, a, b)

            print(f"Result: {result}")
            conn.sendall(package.numberToBinary(result).tobytes())
            #conn.sendall(b"Dostalem operacje: " + operation + b"\n\
            #Wynik to: " + str(result))



#wait = input("PRESS ENTER TO CONTINUE.")