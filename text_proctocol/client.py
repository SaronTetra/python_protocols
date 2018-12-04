import socket

import datagram

print("""
########################
#       CLIENT         #
########################""")

### PYTANIA ###
#
#   Jaki znacznik czasu, sekundy?
#       tak
#   Czy można założyć, że pola zawsze są w tej samej kolejności i zawsze jest ich tyle samo?
#       nie
#
#   Czy robić ACK?
#       tak
#   Czy klienci zgadują na zmianę?
#       nie
#   Pozostałe próby/podpowiedzi jako osobne pole?
#       tak - tylko wartość
#
#


# if (sys.argv[1] == 'm'):
#     HOST = '192.168.0.20'
# else:
HOST = '127.0.0.1'
PORT = 6666

target = (HOST, PORT)

# Establish ID
send = datagram.pack("ID", "", "", "")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    datagram.send(s, send, target)
except socket.error:
    print("Connection lost")

data, server = s.recvfrom(1024)
print(f"Server reply: {data} \n---------")

fields = datagram.unpack(data)
print(fields)
ID = 0
if fields["op"] == "ID":
    ID = fields["id"]
# send = datagram.pack("test", "", ID)
# s.sendto(send.encode('ascii'), (HOST, PORT))

datagram.send(s, datagram.pack("ACK", "", fields["op"], ""), target, True)

print(f"My ID: {ID}")


# ID should be established, main program here

wait = True

while True:
    op = ""

    print("Waiting for server...")
    data, server = s.recvfrom(1024)
    wait = False
    if data:
        fields = datagram.unpack(data)
        op = fields["op"]
        if op != "ACK":
            datagram.send(s, datagram.pack("ACK", "", op, ID), server, True)
        if op == "ACK":
                continue
        elif op == "wait":
            wait = True
            continue
        elif op == "begin":
            l = input("Please enter an even natural number: ")
            datagram.send(s, datagram.pack("attnum", l, "", ID), target)
            wait = True
        elif op == "guess":
            l = input("Input number: ")
            datagram.send(s, datagram.pack("guess", l, "", ID), target)
            wait = True
        elif op == "lose":
            print("Out of attempts")
            break
        elif op == "win":
            print("You guess the number!")
            break;
s.close()
