import send_message
import random

def generate_random_number(path: str):
    with open(path, 'r') as file: 
        lines = file.readlines()   
    return random.choice(lines).strip(), random.choice(lines).strip() 

file_path = "nombres_premiers.txt"

p,g = generate_random_number(file_path)

def decrypt(sock, reponse_func, encoded_message):
        sock.send(encoded_message)
        reponse_func()
        p = 23
        g = 5
        a = 4
        m = f"23,5"
        m = send_message.message_to_int(m)
        m = send_message.encode_message(b's',m)
        sock.send(m)
        reponse_func()
        r = reponse_func()
        half = half_key(p,g,a)
        m = send_message.message_to_int(str(half))
        m = send_message.encode_message(b's', m)
        sock.send(m)
        reponse_func()
        commun = clef(int(r),int(p),int(a))
        m = send_message.message_to_int(str(commun))
        m = send_message.encode_message(b's',m)
        sock.send(m)
        reponse_func()

def half_key(p: int, g: int, a: int):
     return pow(g,a,p)

def clef(number: int, p: int, a: int):
    return pow(number, a, p)


#DH Ok
#Faire les randoms keys