import socket
import send_message
import shift
import time

#Fonction réponse
def reponse():
    data = sock.recv(1024)
    reponse = data.decode('utf-8').strip()
    reponse = reponse.replace('\x00', '')

    if reponse.startswith("ISCs") or reponse.startswith("ISCt"):
        reponse = reponse[5:].strip()
    
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
TASK = "shift"
TYPE = "encode"
message = f"task {TASK} {TYPE} 6"
#message = f"test"

encoded_message = send_message.encode_message(M, message)

if(M == b't'):
    sock.send(encoded_message) 
    reponse()
else:
    if(TASK == "shift" and TYPE == "encode"):
        shift.encode(sock, reponse, encoded_message)
    else:
        shift.decode(sock, reponse, encoded_message)

sock.close()