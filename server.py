import socket
import package
from bitstring import BitArray, BitStream

print("""
########################
#       SERVER         #
########################""")


#Connection variables
HOST = '127.0.0.1'
#HOST = '192.168.0.20'
PORT = 4666
flag =socket.SHUT_RDWR

#Creating socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))

#Waiting for connection
    print("Listening")
    s.listen()

#Accepting connection
    conn, addr = s.accept()
    with conn:
        print("Connected by", addr)

#Generate and send session id
        sessionID = BitArray()
        sessionID = package.IDGen()
        idPack = package.pack('+', 0, 0, 1, sessionID)
        print (f"Sending session ID: {idPack.bin[0:3]} {idPack.bin[3:35]} {idPack.bin[35:67]}",
        f" {idPack.bin[67:69]} {idPack.bin[69:77]} {idPack.bin[77:]}")
        conn.send(idPack.tobytes())

        while True:
            data = BitArray()
            data.append(conn.recv(1024))
            if not data:
                break

            print(f"Recieved: {data.bin[0:3]} {data.bin[3:35]}", 
            f"{data.bin[35:67]} {data.bin[67:69]} {data.bin[69:77]}",
            f"{data.bin[77:]}\nData size: {data.len}")
            
#Operating on recieved data
            operation = data[0:3].bin
            a = data[3:35].int
            b = data[35:67].int
            status = data[67:69]
            clientID = data[69:77].bin
            print(f"A: {a}, B:{b}")
            status = data[67:69]
            id = data[69:77]
            

            # while x != 'q':
            # x = input("Commands pls ")
            print("Operation: " + str(operation))
            result = package.countTwo(operation, a, b)
            #TODO: checking whether number is less than or equal to 32 bits

#TODO: recieve loop, more than two arguments
#Sending result to client
            print(f"Result: {result}")
            conn.sendall(package.numberToBinary(result, 32).tobytes())


#End connection
    #s.shutdown(flag)
    s.close()

#wait = input("PRESS ENTER TO CONTINUE.")