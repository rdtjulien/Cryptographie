import protocol
import random

def generate_random_number(path: str):
    with open(path, 'r') as file: 
        lines = file.readlines()   
    return random.choice(lines).strip(), random.choice(lines).strip() 

file_path = "nombres_premiers.txt"

p,g = generate_random_number(file_path)

def decrypt(sock, reponse_func, encoded_message):
        protocol.send(sock,encoded_message)
        print(protocol.receive(sock))
        p = 23
        g = 5
        a = 4
        m = f"23,5"
        m = protocol.str_to_int_list(m)
        m = protocol.wrap_message(b's',m)
        print(protocol.send(sock,m))
        protocol.receive(sock)
        r = protocol.receive(sock)
        print(r)
        half = half_key(p,g,a)
        m = protocol.str_to_int_list(str(half))
        m = protocol.wrap_message(b's', m)
        protocol.send(sock, m)
        print(protocol.receive(sock))
        commun = clef(int(r),int(p),int(a))
        m = protocol.str_to_int_list(str(commun))
        m = protocol.wrap_message(b's',m)
        protocol.send(sock,m)
        print(protocol.receive(sock))

def half_key(p: int, g: int, a: int):
     return pow(g,a,p)

def clef(number: int, p: int, a: int):
    return pow(number, a, p)


#DH Ok
#Faire les randoms keys