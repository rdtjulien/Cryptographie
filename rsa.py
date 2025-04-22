import send_message
import math
import random

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

def encrypt(sock, reponse_func, encoded_message):
    sock.send(encoded_message)
    m = reponse_func()
    e, n = recup_key(m)
    msg = reponse_func()
    encode_msg = encode_RSA(msg, e, n)
    encode_msg = send_message.encode_message(b's', encode_msg)
    print(encode_msg)
    sock.send(encode_msg)
    reponse_func()

#bricolage à refaire
def decrypt(sock, reponse_func, encoded_message):
        sock.send(encoded_message)
        reponse_func()
        p,q = generate_random_number(file_path)
        n,e,d = generate_key(3,7)
        m = f"{n},{e}"
        m = send_message.message_to_int(m)
        m = send_message.encode_message(b's',m)
        sock.send(m)
        r = reponse_func()
        r = encode_RSA(r, d, n)
        print(r)
        message = send_message.encode_message(b's', r)
        sock.send(message)
        reponse_func()

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

def generate_random_number(path: str):
    with open(path, 'r') as file: 
        lines = file.readlines()   
    return random.choice(lines).strip(), random.choice(lines).strip() 

file_path = "nombres_premiers.txt"

p,q = generate_random_number(file_path)


#Encode Ok
#fix (refaire) decode et faire clée aléatoire
#Refaire la fonction generate_key()