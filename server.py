import socket
import package
import errors
from bitstring import BitArray, BitStream

print("""
########################
#       SERVER         #
########################""")


#Connection variables
HOST = '127.0.0.1'
#HOST = '192.168.0.21'
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
        clientID = BitArray()
        clientID = package.IDGen(conn)
        serverID = BitArray(8)

        result = 0
        loop = True
        while loop:
            data = BitArray()
            data.append(conn.recv(1024))
            if not data:
                break

            print (f"Recieved: {data.bin[0:3]} {data.bin[3:35]} {data.bin[35:37]}",
                f" {data.bin[37:45]} {data.bin[45:46]} {data.bin[46:47]} {data.bin[47:]}")
            
            first = int(data[46])
            #print(f"First: {first}")
            last = int(data[45])
            operation = data[0:3].bin
            #operation = '-'
            packg = BitArray()
            if first == 1:
                result = data[3:35].int
                print(f"Server result: {result}")
                packg = package.pack('+', result, 0, serverID, last, first, 0)
            elif first == 0 and last == 0:            
                a = data[3:35].int
                #print(f"MOJE DATA a: {a}")
                try:
                    result = package.countTwo(operation, result, a)
                except errors.DivisionByZeroException as err:
                    print(f"Exception code: {err}")
                    packg = package.pack('+', 0, 3, serverID, 1, 0, 1)
                    loop = False
                except errors.BinomalTheoremException as err:
                    print(f"Exception code: {err}")
                    packg = package.pack('+', 0, 3, serverID, 1, 0, 3)
                    loop = False
                else:
                    if result < -2147483648 or result > 2147483647:
                        print(f"Exception code: 2")
                        packg = package.pack('+', 0, 3, serverID, 1, 0, 2)
                        loop = False
                    elif isinstance(result, float):
                        print("Isinstance")
                        packg = package.pack('+', round(result), 2, serverID, last, first, 0)
                    else:
                        print("normal")
                        packg = package.pack('+', result, 0, serverID, last, first, 0)
            elif last == 1:
                a = data[3:35].int
                try:
                    result = package.countTwo(operation, result, a)
                except errors.DivisionByZeroException as err:
                    print(f"Exception code: {err}")
                    packg = package.pack('+', 0, 3, serverID, 1, 0, 1)
                    loop = False
                except errors.BinomalTheoremException as err:
                    print(f"Exception code: {err}")
                    packg = package.pack('+', 0, 3, serverID, 1, 0, 3)
                    loop = False
                else:
                    if result < -2147483648 or result > 2147483647:
                        print(f"Exception code: 2")
                        packg = package.pack('+', 0, 3, serverID, 1, 0, 2)
                        loop = False
                    elif isinstance(result, float):
                        print("Isinstance")
                        packg = package.pack('+', round(result), 2, serverID, last, first, 0)
                        loop = False
                    else:
                        print("Normal")
                        packg = package.pack('+', result, 0, serverID, last, first, 0)
                        loop = False

            print (f"Sending:  {packg.bin[0:3]} {packg.bin[3:35]} {packg.bin[35:37]}",
                f" {packg.bin[37:45]} {packg.bin[45:46]} {packg.bin[46:47]} {packg.bin[47:]}")
            conn.sendall(packg.tobytes())

            
        print(f"Result: {result}")


#End connection
    #s.shutdown(flag)
    conn.close()

#wait = input("PRESS ENTER TO CONTINUE.")