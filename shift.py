import re
import send_message

#Récupère le k
def shift_key(reponse: str):
    numbers = re.findall(r'\d+', reponse)
    return int("".join(numbers))

#Encode le message
def trans_shift(reponse: str, k: int):
    temp = []
    for i in reponse:
        i = ord(i) + int(k)
        temp.append(chr(i))
    temp = ''.join(temp)
    return temp

#Decoder le message
def shift_encode(reponse: str):
    temp = []
    for i in reponse:
        i = ord(i) - 6
        temp.append(chr(i))
    return ''.join(temp)

#Envoie au serveur pour l'encodage
def encode(sock, reponse_func, encoded_message):
    sock.send(encoded_message)
    k = reponse_func()
    k = shift_key(k)
    serv_reponse = reponse_func()
    shift_message = trans_shift(serv_reponse, int(k))
    print(f"Shift message: {shift_message}")
    shift_message = send_message.encode_message(b's', shift_message)
    sock.send(shift_message)
    serv_reponse = reponse_func()

#Envoie au serveur pour le decodage
def decode(sock, reponse_func, encoded_message):
    sock.send(encoded_message)
    reponse_func()
    message_encoder = reponse_func()
    shift_message = shift_encode(message_encoder)
    print(f"Shift message: {shift_message}")
    shift_message = send_message.encode_message(b's', shift_message)
    sock.send(shift_message)
    reponse_func()
