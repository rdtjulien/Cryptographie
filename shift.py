import re
import protocol
import send_message

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

#Envoie au serveur pour l'encodage
def encode(sock, encoded_message, reponse):
    protocol.send(sock, encoded_message)
    k = reponse()
    key = shift_key(k)
    serv_reponse = reponse()
    shift_message = trans_shift(serv_reponse, int(key))
    shift_message = protocol.wrap_message(shift_message)
    protocol.send(sock, shift_message)
    reponse()
#Ok