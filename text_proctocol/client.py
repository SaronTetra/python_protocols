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
#
#   Czy klienci zgadują na zmianę?
#
#   Pozostałe próby/podpowiedzi jako osobne pole?
#
#
#


# if (sys.argv[1] == 'm'):
#     HOST = '192.168.0.20'
# else:
HOST = '127.0.0.1'

PORT = 6666
# Establish ID
send = datagram.pack("ID", "", "")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    s.sendto(send.encode('ascii'), (HOST, PORT))
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

print(f"My ID: {ID}")


# ID should be established, main program here

def send(data):
    s.sendto(data.encode("ascii"), (HOST, PORT))


wait = True

while True:
    op = ""
    if not wait:
        x = input(">")
        if x == "x":
            break
        elif x == "id":
            print(f"My ID: {ID}")
            continue
        # elif x == "":
        send(datagram.pack(x, "", ID))

    print("Waiting for server...")
    data, server = s.recvfrom(1024)
    wait = False
    if data:
        fields = datagram.unpack(data)
        op = fields["op"]
        if op == "test":
            send = datagram.pack(op, "Hello there!", ID)
        elif op == "wait":
            wait = True
            continue
        elif op == "begin":
            l = input("Please enter an even natural number: ")
            send(datagram.pack("attnum", l, ID))
            wait = True
        elif op == "guess":
            l = input("Input number: ")
            send(datagram.pack("guess", l, ID))
            wait = True
        elif op == "lose":
            print("Out of attempts")
            break
        elif op == "win":
            print("You guess the number!")
s.close()
