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
    s.close()
    with conn:
        print("Connected by", addr)

#Generate and send session id
        ID = BitArray()
        ID = package.IDGen(conn)

        result = 0
        loop = True
        while loop:
            data = BitArray()
            data.append(conn.recv(1024))
            if not data:
                break

            print(f"Recieved: {data.bin[0:3]} {data.bin[3:35]}", 
            f"{data.bin[35:67]} {data.bin[67:69]} {data.bin[69:77]}",
            f"{data.bin[77:]}\tData size: {data.len}")
            
            

            #TODO: some id verification?
            if data.len == 80:

                print(f"Recieved: {data.bin[0:3]} {data.bin[3:35]}", 
                f"{data.bin[35:67]} {data.bin[67:69]} {data.bin[69:77]}",
                f"{data.bin[77:]}\tData size: {data.len}")
                status = abs(data[67:69].int)
                if status == 1:

                    operation = data[0:3].bin
                    a = data[3:35].int
                    b = data[35:67].int
                    status = data[67:69]
                    clientID = data[69:77].bin
                    print(f"A: {a}, B:{b}")

                    print("Operation: " + str(operation))
                    result = package.countTwo(operation, a, b)
                    pack = BitArray()
                    pack = package.packOne('+', result, 2, ID, 0)
                    conn.sendall(pack.tobytes())
                    loop = False


                elif status == 0:
                    operation = data[0:3].bin
                    a = data[3:35].int
                    b = data[35:67].int
                    status = data[67:69]
                    clientID = data[69:77].bin
                    print(f"A: {a}, B:{b}")

                    print("Operation: " + str(operation))
                    result = package.countTwo(operation, a, b)
                    pack = BitArray()
                    pack = package.packOne('+', result, 2, ID, 0)
                    conn.sendall(pack.tobytes())

                    #TODO: checking whether number is less than or equal to 32 bits
            elif data.len == 48:
                status = abs(data[35:37].int)
                
                print(f"Recieved: {data.bin[0:3]} {data.bin[3:35]}", 
                f"{data.bin[35:37]} {data.bin[37:45]} {data.bin[45:]}")
                if status == 1:

                    operation = data[0:3].bin
                    a = data[3:35].int           
                    clientID = data[37:45].bin
                    print(f"A: {a}, B:{b}")

                    print("Operation: " + str(operation))
                    result = package.countTwo(operation, result, a)
                    pack = BitArray()
                    pack = package.packOne('+', result, 2,ID, 0) #TODO: Last result
                    conn.sendall(pack.tobytes())
                    loop = False
                
                elif status == 0:
                    operation = data[0:3].bin
                    a = data[3:35].int           
                    clientID = data[37:45].bin
                    print(f"A: {a}, B:{b}")

                    print("Operation: " + str(operation))
                    result = package.countTwo(operation, result, a)
                    pack = BitArray()
                    pack = package.packOne('+', result, 2, ID, 0)
                    conn.sendall(pack.tobytes())

            
        print(f"Result: {result}")


#End connection
    #s.shutdown(flag)
    conn.close()

#wait = input("PRESS ENTER TO CONTINUE.")