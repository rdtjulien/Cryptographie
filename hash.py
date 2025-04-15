import send_message
import hashlib

def encrypt(sock, reponse_func, encoded_message):
    sock.send(encoded_message)
    reponse_func()
    r = reponse_func()
    r = send_message.message_to_int(r)
    r = send_message.encode_message(b's', r)
    m = hashlib.sha256()
    m = m.digest()
    r = add_ISC(b's', m)
    print(r)
    sock.send(r)
    reponse_func()

def add_ISC(m:bytes, message:str):
    length = len(message)
    prefix = b'ISC'
    length = length.to_bytes(2, 'big')
    
    return prefix + m + length + message

s = "ue par les théologiens chrétiens. En réalité, les"
s = send_message.message_to_int(s)
s = send_message.byte_message(s)
s = hashlib.sha256()
s = s.digest()
s = add_ISC(b's', s)
print(s)


#Hash hash fixe problème