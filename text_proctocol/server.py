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
#HOST = '192.168.0.20'

PORT = 6666

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))


while True:
    data, address = s.recvfrom(1024)
    if data:
        fields = datagram.unpack(data)
        op = fields["op"]
        if op == "ID":
            ID = datagram.generateID();
            send = datagram.pack("ID", ID, 0)
        elif op == "test":
            send = datagram.pack(op, "Hello there!", 0)
        else:
            send = datagram.pack("info", "Invalid command", 0)
        print("got data", data)
    s.sendto(send.encode("ascii"), address)

