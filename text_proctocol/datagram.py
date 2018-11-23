import random
import time
import re


def generateID():
    return random.randrange(1, 256)


def pack(op, response, ID):
    result = ""
    if op:
        result += f"Operacja>{str(op)}<"
    if response:
        result += f"Odpowiedz>{str(response)}<"
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

def show(fields):
    print(f'{fields["time"]}[{fields["id"]}] - {fields["op"]}: {fields["resp"]} ')


def unpack(data):
    m = re.findall(r"([a-zA-Z]+)>(.*?)<", str(data))
    fields = {
        "op": "",
        "resp": "",
        "id": "",
        "time": ""
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
    show(fields)
    return fields
