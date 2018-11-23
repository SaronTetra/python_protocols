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
paddr = []
l = 0
attempts = 0
secretNumber = 0
turn = 0

while True:
    op = ""
    data, address = s.recvfrom(1024)

    if data:
        fields = datagram.unpack(data)
        op = fields["op"]
        if op == "ID":
            ID = datagram.generateID();
            players.append(ID)
            paddr.append(address)
            send = datagram.pack("ID", "", ID)
            s.sendto(send.encode("ascii"), address)
            if len(players) >= 2:
                send = datagram.pack("begin", "", players[0])
                s.sendto(send.encode("ascii"), paddr[0])
                send = datagram.pack("begin", "", players[1])
                s.sendto(send.encode("ascii"), paddr[1])
            continue
        elif op == "attnum":
            l += int(fields["resp"])
            print(f"got: {fields['resp']} ")
            send = datagram.pack("wait", "", fields["id"])
            turn += int(fields["id"])
            if turn == players[0] + players[1]:
                attempts = l / 2
                secretNumber = random.randrange(1, 10000)
                send = datagram.pack("guess", attempts, players[0])
                s.sendto(send.encode("ascii"), paddr[0])
                send = datagram.pack("guess", attempts, players[1])
                s.sendto(send.encode("ascii"), paddr[1])
                turn = 0
                print(f'"secret" number is {secretNumber}')

        elif op == "guess":
            attempts -= 1
            if attempts < 0:
                send = datagram.pack("lose", "", fields["id"])
            if int(fields["resp"]) == secretNumber:
                send = datagram.pack("win", "", fields["id"])
            else:
                if int(fields["resp"]) > secretNumber:
                    hint = "lower"
                else:
                    hint = "higher"
                send = datagram.pack("guess", f'{hint} - {attempts} left', fields["id"])
        else:
            send = datagram.pack("info", "Invalid command", 0)
    s.sendto(send.encode("ascii"), address)


