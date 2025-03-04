import socket
import time as ornithorynque
import shift

#Partie connection serveur
PORT = 6000
ADDRESS = 'vlbelintrocrypto.hevs.ch'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((ADDRESS, PORT))
except Exception as e:
    print("Cannot connect to the server:", e)
print("Connected")

#Partie Tranfo mot en byte
ISC = "ISC"
M = 't'

# entrer le texte qu'on veut
print("mot de base")
#message1 = input("Message: ")
message = "hello"
message1 = message
print(message1)

#définir taille du message + Hex
bytes_val = shift.taille_message(message)

# transforme en byte char by char
message1 = shift.byte_to_char(message)

#transformer en Int
message1 = shift.trans_to_int(message1)

#faire les manipulations sur les INT
message1 = shift.manip_int(message1)

#re transformer en Byte
message1 = shift.re_trans_to_byte(message1)

#Transfo en Hex pour le bon format de transmission
message1 = shift.trans_byte_to_hex(message1)

#mettre en forme le message et transmettre (encapsuler)
message_trans = shift.encapsulation(ISC, M, bytes_val, message1)

#Transmission Serveur
sock.send(message_trans.encode())

tic = ornithorynque.perf_counter()
reponse = sock.recv(1024)
print(f"réponse: {reponse.decode("utf-8")}")
toc = ornithorynque.perf_counter()
print(f"{toc - tic:0.4f} seconds")
sock.close