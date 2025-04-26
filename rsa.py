import protocol
import math

# ==========================
# Outils de chiffrement RSA
# ==========================

def power(base, expo, m):
    """Effectue un calcul modulaire : base^expo % m"""
    return pow(base, expo, m)

def recup_key(serv_msg):
    """
    Récupère les clés publique e et n depuis un message du serveur.
    Format attendu : "...=n=e"
    """
    mod = serv_msg.split('=')
    n = mod[1][:-3]  # Enlève le suffixe ou fin de chaîne parasite
    e = mod[2]
    return e, n

def encode_RSA(message: str, e, n):
    """
    Chiffre chaque caractère du message avec RSA.
    Chaque caractère est transformé en entier, puis chiffré : c = m^e mod n
    """
    temp = []
    for char in message:
        i = int.from_bytes(char.encode(), 'big')
        i = power(i, int(e), int(n))
        temp.append(i)
    return temp

# ========================
# Envoi du message chiffré
# ========================

def encrypt(sock, encoded_message, reponse_func):
    """
    Étapes :
    1. Envoie la commande au serveur pour déclencher RSA.
    2. Récupère les clés publiques e, n.
    3. Récupère le message à chiffrer.
    4. Chiffre avec RSA et envoie au serveur.
    """
    protocol.send(sock, encoded_message)
    m = reponse_func()  # réponse contenant les clés
    e, n = recup_key(m)
    msg = reponse_func()  # message clair à chiffrer
    encode_msg = encode_RSA(msg, e, n)
    protocol.send(sock, protocol.wrap_message(encode_msg))
    reponse_func()

# ==========================
# Réception et déchiffrement
# ==========================

def decrypt(sock, reponse_func, encoded_message):
    """
    Étapes :
    1. Envoie la commande pour déchiffrement RSA.
    2. Génère une paire de clés RSA (aléatoirement via nombres premiers).
    3. Envoie n et e au serveur.
    4. Récupère le message chiffré.
    5. Déchiffre avec la clé privée d, et renvoie au serveur.
    """
    protocol.send(sock, encoded_message)
    reponse_func()

    # Génère deux nombres premiers p et q aléatoires
    p, q = protocol.get_random_primes()
    n, e, d = generate_key(p, q)

    # Envoie n et e (clé publique) au serveur
    key_msg = f"{n},{e}"
    protocol.send(sock, protocol.prepare_message(key_msg))

    # Réception du message chiffré
    encrypted_msg = reponse_func()

    # Déchiffre le message avec la clé privée d
    decrypted_ints = encode_RSA(encrypted_msg, d, n)
    protocol.send(sock, protocol.wrap_message(decrypted_ints))

    reponse_func()

# =====================
# Génération des clés
# =====================

def generate_key(p: int, q: int):
    """
    Génère les clés RSA (n, e, d) à partir de deux nombres premiers p et q.
    - n = p * q
    - e : un entier premier avec (p-1)*(q-1)
    - d : l'inverse modulaire de e modulo phi
    """
    n = p * q
    phi = (p - 1) * (q - 1)

    # Trouver e coprime avec phi
    for e in range(3, phi):
        if math.gcd(e, phi) == 1:
            break

    # Trouver d tel que (d * e) % phi == 1
    for d in range(3, phi):
        if (d * e) % phi == 1:
            return n, e, d

    raise Exception("Clé RSA invalide")



