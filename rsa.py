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
        m = "9845984,9023483"
        n = 9845984
        e = 9023483
        length = len(m)
        m = send_key(m)
        m = encode_message_RSA(b's',m, length)
        sock.send(m)
        r = reponse_func()
        p,q = p_q(n)
        print(f"p et q {p,q}")
        p_i = (p-1)*(q-1)
        print(f"phi : {p_i}")
        d = pow(e, -1, p_i)
        print(d)
        x = d_RSA(r, d, n)
        print(x)
        x = encode_message_RSA(b's', x, 10)
        print(x)
        sock.send(x)
        reponse_func()


def send_key(m: str):
    temp = []
    for i in m:
        i = i.encode()
        i = int.from_bytes(i)
        temp.append(i)
    return temp

m = "9845984,9023483"
n = 9845984
e = 9023483
code = "8ڠ`c►2ic↨&`K"

n = len(m)

l = send_key(m)
v = encode_message_RSA(b's', l, n)

print(v)


def p_q(n):
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            p = i
            q = n // i
            break
    return p,q

def d_RSA(m:str, d, n):
    temp = []
    for i in m:
        i = i.encode()
        i = int.from_bytes(i)
        decode = pow(i, d,n)
        temp.append(decode)
    return temp

n = 9845984
e = 9023483
code = "8ڠ`c►2ic↨&`K"

p = 2
q = 5

p_i = (p-1)*(q-1) 
print(p_i)

d = pow(e, -1, p_i)
print(d)

x = d_RSA(code, d, n)
print(x)