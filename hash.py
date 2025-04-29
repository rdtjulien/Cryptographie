import send_message
import hashlib
import protocol


def hash(sock, encoded_message, reponse_func):
    sock.send(encoded_message)
    reponse_func()
    r = reponse_func()
    m = hashlib.sha256(r.encode('utf-8')).hexdigest()
    hash_bytes = str(m)
    hash_int = send_message.message_to_int(hash_bytes)
    final_message = send_message.encode_message(b's', hash_int)
    sock.sendall(final_message)
    reponse_func()


def verify(sock, encoded_message, reponse_func):
    sock.send(encoded_message)
    reponse_func()
    r = reponse_func()
    texte = separer_texte(r)
    hash_texte = hashlib.sha256(texte[0].encode('utf-8')).hexdigest()

    if hash_texte == texte[1]:
        rep = "true"
    else :
        rep = "false"
    d = send_message.message_to_int(rep)
    d = send_message.encode_message(b's', d)
    sock.send(d)
    reponse_func()

def separer_texte(chaine):
    texte_separe = chaine.split("ISCs@")
    
    return texte_separe
