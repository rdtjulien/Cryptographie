import socket
import send_message
import shift
import time
import Vigenere
import rsa
import dh
import hash

#Fonction réponse
def reponse():
    data = sock.recv(1024)
    reponse = data.decode('utf-8', errors='ignore').strip()
    reponse = reponse.replace('\x00', '')

    if reponse.startswith("ISCs") or reponse.startswith("ISCt"):
        reponse = reponse[5:]
    
    print(f"Réponse serveur : {reponse}")
    return reponse

# Partie connection serveur
PORT = 6000
ADDRESS = 'vlbelintrocrypto.hevs.ch'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((ADDRESS, PORT))
    print("Connected")
except Exception as e:
    print("Cannot connect to the server")

M = b's'
TASK = "RSA"
TYPE = "encode"
LENGTH = 10
message = f"task {TASK} {TYPE} {LENGTH}"
#message = f"task {TASK}"
#message = f"task {TASK} {TYPE}"
#message = f"Salut"

message = send_message.message_to_int(message)
encoded_message = send_message.encode_message(M, message)

if(M == b't'):
    sock.send(encoded_message)
    reponse()
else:
    if(TASK == "shift" and TYPE == "encode"):
        shift.encode(sock, reponse, encoded_message)
    elif(TASK == "vigenere" and TYPE == "encode"):
        Vigenere.encode(sock, reponse, encoded_message)
    elif(TASK == "RSA" and TYPE == "encode"):
        rsa.encrypt(sock, reponse, encoded_message)
    elif(TASK == "RSA" and TYPE == "decode"):
        rsa.decrypt(sock, reponse, encoded_message)
    elif(TASK == "DifHel"):
        dh.decrypt(sock,reponse,encoded_message)
    elif(TASK == "hash" and TYPE == "hash"):
        hash.encrypt(sock,reponse, encoded_message)

sock.close()
