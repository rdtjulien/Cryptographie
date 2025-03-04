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
"""""
i = 'I'.encode()
s = 'S'.encode()
c = 'C'.encode()

isc = f"{i}{s}{c}"
"""
isc = "ISC"
m = 's'

# entrer le texte qu'on veut
print("mot de base")
#message1 = input("Message: ")
message = "hello"
message1 = message
print(message1)
#définir taille du message + Hex
length_string = int(len(message))
bytes_val = length_string.to_bytes(2,'big')
bytes_val = bytes_val.hex().upper()
print(f"LongueurMessageHex : \n{bytes_val}")  


# transforme en byte char by char
message1 = list(message1)
temp = []
encode = ""

for i in message1:
    encode = i.encode('utf-8')
    temp.append(encode)
print(f"transfoChar : \n{temp}")
message1 = temp

#transformer en Int
list_to_int = 0
modif_message = []

for i in message1:
    list_to_int = int.from_bytes(i,'big')
    modif_message.append(list_to_int)
print(f"ListInt : \n{modif_message}")

#faire les manipulations sur les INT
k = 0
temp = []
for i in modif_message:
    x = i << k
    temp.append(x)
print(f"ManipInt : \n{temp}")
message1 = temp

#re transformer en Byte
temp = []
for i in message1:
    c = i.to_bytes(4,'big')
    temp.append(c)
print(f"ReTransfoByte : \n{temp}")    
message1 = temp
#Transfo en Hex pour le bon format de transmission

full_data = b''.join(message1)
message1 = full_data.hex().upper()
print(f"trandsfoByteToHex : \n{message1}")  



#mettre en forme le message et transmettre (encapsuler)

message_trans = f'{isc}{m}{bytes_val}{message1}'
print(f"message: \n{message_trans}")
print(f'modèle : \nISCs000500000068000000650000006C0000006C0000006F')
#message = f'ISCs000500000068000000650000006C0000006C0000006F'

#Transmission Serveur
sock.send(message_trans.encode())

reponse = sock.recv(1024)
print(f"réponse: {reponse.decode("utf-8")}")

sock.close
