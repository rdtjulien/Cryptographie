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
        i = i.encode()
        i = int.from_bytes(i)
        i = i + k
        temp.append(i)
    return temp

#Envoie au serveur pour l'encodage
def encode(sock, reponse_func, encoded_message):
    sock.send(encoded_message)
    k = reponse_func()
    print(k)
    k = shift_key(k)
    print(k)
    serv_reponse = reponse_func()
    shift_message = trans_shift(serv_reponse, int(k))
    shift_message = send_message.encode_message(b's', shift_message)
    sock.send(shift_message)
    print(shift_message)
    serv_reponse = reponse_func() 

#Ok