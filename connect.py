import socket

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
i = 'I'.encode()
s = 'S'.encode()
c = 'C'.encode()

isc = f"{i}{s}{c}"

m = 's'.encode()

# entrer le texte qu'on veut
print("mot de base")
#message1 = input("Message: ")
message = "hello worldé"
message1 = message
print(message1)

# transforme en byte char by char
message1 = list(message1)
temp = []
encode = ""
k = 1

for i in message1:
    encode = i.encode('utf-8')
    temp.append(encode)
message1 = temp

list_to_int = 0
modif_message = []

#transformer en Int
for i in message1:
    list_to_int = int.from_bytes(i,'big')
    modif_message.append(list_to_int)

#faire les manipulations sur les INT
temp = []
for i in modif_message:
    x = i + k
    temp.append(x)
message1 = temp

#re transformer en Byte
temp = []
for i in message1:
    c = i.to_bytes(4,'big')
    temp.append(c)
message1 = temp

new_message = ""
for i in message1:
    new_message += str(i)
message1 = new_message

#mettre en forme le message et transmettre
length_string = int(len(message))
bytes_val = length_string.to_bytes(2,'big')

message = f'{isc}{m}{bytes_val}{message1}'
#message = f'ISCs000500000048000000650000006C0000006C0000006F'
print(f"message: {message}")
"""""
sock.send(message.encode())

reponse = sock.recv(1024)
print(f"réponse: {reponse.decode("utf-8")}")

sock.close
"""""