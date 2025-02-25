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
print("convertion byte")
message1 = message1.encode('utf-8')
print(message1)
# mettre les byte dans un tableau
print("mise en tableau")
message1 = list(message1)
print(message1)
#transformer en Int
#faire les manipulations sur les INT
#re transformer en Byte

#mettre en forme le message et transmettre

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

#Ceci est un test de commit pull push git ta mère salut

