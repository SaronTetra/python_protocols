import random
import socket
import re

from text_proctocol import datagram

print("""
########################
#       SERVER         #
########################""")

# Temat: Komunikacja pomiędzy klientami poprzez serwer (2:1),
#  w oparciu o autorski protokół# tekstowy.

# Protokół:
# - bezpołączeniowy,
# - wszystkie dane przesyłane w postaci tekstowej (sekwencja znaków ASCII),
# - każdy komunikat opatrzony znacznikiem czasu,
# - struktura elementów nagłówka zdefiniowana jako klucz>wartość<
#   - (przykład) Operacja>dodaj<
# - wymagane pola:
#   - pole operacji – „Operacja”,
#   - pole odpowiedzi – „Odpowiedz”,
#   - pole identyfikatora – „Identyfikator”.
# - dodatkowe pola zdefiniowane przez programistę.

# Operacja><Odpowiedz><Identyfikator><Czas><

# Funkcje oprogramowania:
# - klienta:
#   - nawiązanie połączenia z serwerem,
#   - uzyskanie identyfikatora sesji,
#   - przesłanie pojedynczej, parzystej liczby naturalnej L,
#   - przesyłanie wartości liczbowych, będących „odpowiedziami”:
#       - klient ma odgadnąć liczbę wylosowaną przez serwer.
#   - zakończenie połączenia.

# - serwera:
#   - wygenerowanie identyfikatora sesji,
#   - wyznaczenie liczby prób od podjęcia ((L1 + L2) / 2 = liczba prób),
#   - wylosowanie liczby tajnej,
#   - przesłanie maksymalnej liczby prób odgadnięcia wartości tajnej,
#   - informowanie klientów, czy wartość została odgadnięta.

# Inne:
#   - identyfikator sesji powinien być przesyłany w trakcie komunikacji,
#   - każdy wysłany komunikat powinien zostać potwierdzony przez drugą stronę.

HOST = '127.0.0.1'
# HOST = '192.168.0.20'

PORT = 6666

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

players = []
l = 0
attempts = {}
secretNumber = 0
turn = 0
ID = 0
connected = {}

while True:
    op = ""
    data, address = s.recvfrom(1024)
    if data:
        fields = datagram.unpack(data)
        op = fields["op"]
        if fields["id"] != "":
            pid = int(fields["id"])
        if op != "ACK":
            datagram.send(s, datagram.pack("ACK", "", op, fields["id"]), address, True)
        if op == "ACK":
            continue
        if op == "ID":
            ID = datagram.generateID();
            players.append(ID)
            connected[ID] = address
            send = datagram.pack("ID", "", "", ID)
            datagram.send(s, send, address)
            print()
            if len(players) >= 2:
                for k, v in connected.items():
                    send = datagram.pack("begin", "", "", k)
                    datagram.send(s, send, v)
            continue
        elif op == "attnum":
            l += int(fields["resp"])
            print(f"got: {fields['resp']} ")
            send = datagram.pack("wait", "", "", pid)
            turn += int(pid)
            if turn == players[0] + players[1]:
                secretNumber = random.randrange(1, 100)
                for k, v in connected.items():
                    attempts[k] = int(l/2)
                    print(f'KEY IS {k} - {v}')
                    send = datagram.pack("guess", attempts[k], "", k)
                    s.sendto(send.encode("ascii"), v)
                turn = 0
                print(f'"secret" number is {secretNumber}')
                print()

        elif op == "guess":
            attempts[pid] -= 1
            if attempts[pid] <= 0:
                send = datagram.pack("lose", "", "", fields["id"])
                players.pop()
            elif int(fields["resp"]) == secretNumber:
                send = datagram.pack("win", "", "", fields["id"])
                players.pop()
            else:
                if int(fields["resp"]) > secretNumber:
                    hint = "lower"
                else:
                    hint = "higher"
                send = datagram.pack("guess", f'{hint} - {attempts} left', "", fields["id"])
        else:
            send = datagram.pack("info", "Invalid operation", "", 0)
    datagram.send(s, send, address)
    if len(players) == 0:
        print("---KONIEC---")
        break


