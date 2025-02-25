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

# entrer le texte qu'on veut
print("mot de base")
message1 = 'hello worldé'
print(message1)
# transforme en byte char by char
message1 = list(message1)
encode = []
temp = ""

for i in message1:
    temp = i.encode('utf-8')
    encode.append(temp)
message1 = encode
print(message1)

tim = 0
recode = []

for i in message1:
    tim = int.from_bytes(i, 'big')
    # Mettre opérations cryptage ici
    c = tim.to_bytes(4,'big')
    recode.append(c)
print(recode)

#transformer en Int



#faire les manipulations sur les INT
#re transformer en Byte

#mettre en forme le message et transmettre
"""""
message = 'task shift encode 6'
length_string = int(len(message))
bytes_val = length_string.to_bytes(2,'big')

message = f'ISCs000500000048000000650000006C0000006C0000006F'

print(f"message: {message}")
sock.send(message.encode('utf-8'))

reponse = sock.recv(1024)
print(f"réponse: {reponse.decode()}")

sock.close()
#print(bytes(message.encode()))
"""

