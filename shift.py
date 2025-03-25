import re
import send_message

#Bricolage
def byte_message(message: str):
    new_message = []
    for i in message:
        new_message.append(i.to_bytes(4,'big'))

    return b''.join(new_message)

def encode_message_shift(m:bytes, message: str, length: int):
    prefix = b'ISC'
    length = length.to_bytes(2, 'big')
    new_message = byte_message(message)

    return prefix + m + length + new_message


#Récupère le k
def shift_key(reponse: str):
    numbers = re.findall(r'\d+', reponse)
    return int("".join(numbers))

#Encode le message
def trans_shift(reponse: str, k: int):
    temp = []
    for i in reponse:
        i = i.encode()
        i = int.from_bytes(i)
        i = i + k
        temp.append(i)
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
    shift_message = encode_message_shift(b's', shift_message, 10)
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