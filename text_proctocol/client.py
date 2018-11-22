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
if fields["op"] == "ID":
    ID = fields["resp"]
send = datagram.pack("test", "", ID)
s.sendto(send.encode('ascii'), (HOST, PORT))

print(f"My ID: {ID}")
# ID should be established, main program here
while True:
    x = input("Enter operation (x to quit): ")
    if x == 'x':
        break
    elif x == "":
        send = datagram.pack(x, "", ID)
    s.sendto(send.encode("ascii"), server)
    data, server = s.recvfrom(1024)
    if data:
        fields = datagram.unpack(data)
        op = fields["op"]
        # Does this make sense, or is it completely useless?
        # if fields["id"] != ID:
        #     print(f'This data is not for me ({ID}), its for {fields["id"]}')
        #     continue

        if op == "test":
            send = datagram.pack(op, "Hello there!", 0)
        print("got data", data)
s.close()
