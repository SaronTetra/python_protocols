import socket


#HOST = '127.0.0.1'
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
            data = conn.recv(1024)
            if not data:
                break
            print(f"encode: {data}")
            strings = str(data.decode('utf'))
            print(f"decode: {strings}")

            operation = strings[:3]
            a = int(strings[3:19])
            b = int(strings[20:36])

            # while x != 'q':
            # x = input("Commands pls ")
            print("op: " + str(operation))
            x = operation
            if x == "000" :
                result = a + b
            elif x == "001":
                result = a - b
            elif x == "010":
                result = a * b
            elif x == "011":
                if b != 0:
                    result = a / b
                else:
                    result = 0
            print( "wynik: " + str(result))
            conn.sendall(b"Dostalem operacje: " + operation.encode("utf") + b"\n\
            Wynik to: " + str(result).encode("utf"))


print(f"Otrzymałem {num}")
wait = input("PRESS ENTER TO CONTINUE.")