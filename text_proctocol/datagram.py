import random
import time
import re


def generateID():
    return random.randrange(1, 256)


def pack(op, response, val, ID):
    result = ""
    if op:
        result += f"Operacja>{str(op)}<"
    if response:
        result += f"Odpowiedz>{str(response)}<"
    if val:
        result += f"Wartosc>{str(val)}<"
    if ID and ID != 0:
        result += f"Identyfikator>{str(ID)}<"

    currentTime = time.strftime('%H:%M:%S', time.localtime())
    # print(result)
    return f"{result}Czas>{currentTime}<"


#   - pole operacji – „Operacja”,
#   - pole odpowiedzi – „Odpowiedz”,
#   - pole identyfikatora – „Identyfikator”.
#   - pole czas - "Czas"
#   - pole
#   - dodatkowe pola zdefiniowane przez programistę.

# Operacje
#   - ID
#   - info
#   - wait
#   - begin
#   - attnum
#
#
#
#

def show(fields, out=True):
    if out:
        direction = "->"
    else:
        direction = "<-"
    if fields["resp"] == "":
        print(f'{fields["time"]}[{fields["id"]}] {direction} {fields["op"]}: {fields["val"]} ')
    else:
        print(f'{fields["time"]}[{fields["id"]}] {direction} {fields["op"]}: {fields["val"]} | {fields["resp"]}')


def unpack(data, out=False):
    m = re.findall(r"([a-zA-Z]+)>(.*?)<", str(data))
    fields = {
        "op": "",
        "resp": "",
        "id": "",
        "time": "",
        "val" : ""
    }
    for e in m:
        if e[0] == "Operacja":
            fields["op"] = e[1]

        elif e[0] == "Odpowiedz":
            fields["resp"] = e[1]

        elif e[0] == "Identyfikator":
            fields["id"] = e[1]

        elif e[0] == "Czas":
            fields["time"] = e[1]

        elif e[0] == "Wartosc":
            fields["val"] = e[1]
    show(fields, out)
    return fields


# def send(s, data, target):
#     print(f"Sending: {data}")
#     s.sendto(data.encode("ascii"), target)
#     print("Waiting for ACK")
#     data, server = s.recvfrom(1024)
#     fields = unpack(data)
#     if fields["op"] == "ACK":
#         print(f"ACK received for {fields['val']}")


def send(s, data, target, ack=False):
    #print(f"Sending {unpack(data, True)['op']} ", end='')
    unpack(data, True)
    s.sendto(data.encode("ascii"), target)
    if not ack:
        print("Waiting for ACK... ")
        data, server = s.recvfrom(1024)
        fields = unpack(data)
       # if fields["op"] == "ACK":
           # print(f"ACK received for {fields['val']}")