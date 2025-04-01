import send_message
import json
import math

def power(base, expo, m):
   return pow(base,expo,m)

def recup_key(serv_msg):
    number = serv_msg
    mod = number.split('=')
    n = mod[1]
    n = n[:-3]
    e = mod[2]
    return e, n

def encode_RSA(serv_mes:str, e, n):
    temp = []
    for i in serv_mes:
        i = i.encode()
        i = int.from_bytes(i)
        i = power(i, int(e), int(n))
        temp.append(i)
    return temp

def byte_message(message: str):
    new_message = []
    for i in message:
        new_message.append(i.to_bytes(4,'big'))

    return b''.join(new_message)

def encode_message_RSA(m:bytes, message: str, length: int):
    prefix = b'ISC'
    length = length.to_bytes(2, 'big')
    new_message = byte_message(message)

    return prefix + m + length + new_message

def decode_message_RSA(m:bytes, message: str):
    prefix = b'ISC'
    length = len(m).to_bytes(2, 'big')
    new_message = byte_message(message)

    return prefix + m + length + new_message

def encrypt(sock, reponse_func, encoded_message):
    sock.send(encoded_message)
    m = reponse_func()
    e, n = recup_key(m)
    msg = reponse_func()
    encode_msg = encode_RSA(msg, e, n)
    encode_msg = encode_message_RSA(b's', encode_msg, 10)
    print(encode_msg)
    sock.send(encode_msg)
    reponse_func()

#bricolage à refaire
def decrypt(sock, reponse_func, encoded_message):
        sock.send(encoded_message)
        reponse_func()
        n,e,d = generate_key(7,19)
        m = f"{n},{e}"
        m,length = send_key(m)
        m = encode_message_RSA(b's',m, length)
        print(n,e,d)
        sock.send(m)
        r = reponse_func()
        k = encode_RSA(r, d, n)
        message = decode_message_RSA(b's', k)
        print(message)
        sock.send(message)
        reponse_func()

def send_key(m: str):
    length = len(m)
    temp = []
    for i in m:
        i = i.encode()
        i = int.from_bytes(i)
        temp.append(i)
    return temp,length

def generate_key(p:int, q:int):
    n = p * q
    t = (p-1)*(q-1)

    for i in range(1, t):
        e = t%i
        if e != 0:
            break
    e = i

    i=0
    while(True):
        i +=1
        c = i*e%t
        if c == 1:
            break
    d = i

    return n,e,d


