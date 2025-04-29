import protocol
import math

# Outils de chiffrement RSA
def power(base, expo, m):
    return pow(base, expo, m)

def recup_key(serv_msg):
    mod = serv_msg.split('=')
    n = mod[1][:-3]
    e = mod[2]
    return e, n

def encode_RSA(message: str, e, n):
    temp = []
    for char in message:
        i = int.from_bytes(char.encode(), 'big')
        i = power(i, int(e), int(n))
        temp.append(i)
    return temp

# Envoi du message chiffré
def encrypt(sock, encoded_message, reponse_func):
    protocol.send(sock, encoded_message)
    m = reponse_func()
    e, n = recup_key(m)
    msg = reponse_func()
    encode_msg = encode_RSA(msg, e, n)
    protocol.send(sock, protocol.wrap_message(encode_msg))
    reponse_func()

# Réception et déchiffrement
def decrypt(sock, reponse_func, encoded_message):
    protocol.send(sock, encoded_message)
    reponse_func()

    p, q = protocol.get_random_primes()
    n, e, d = generate_key(p, q)

    key_msg = f"{n},{e}"
    protocol.send(sock, protocol.prepare_message(key_msg))

    encrypted_msg = reponse_func()

    decrypted_ints = encode_RSA(encrypted_msg, d, n)
    protocol.send(sock, protocol.wrap_message(decrypted_ints))

    reponse_func()

# Génération des clés
def generate_key(p: int, q: int):
    n = p * q
    phi = (p - 1) * (q - 1)

    for e in range(3, phi):
        if math.gcd(e, phi) == 1:
            break

    for d in range(3, phi):
        if (d * e) % phi == 1:
            return n, e, d

    raise Exception("Clé RSA invalide")



