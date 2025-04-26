import socket
import random
import time

# ========= Données communes =========

file_path = "nombres_premiers.txt"       

def generate_random_number(path: str):
    with open(path, 'r') as file: 
        lines = file.readlines()   
    return random.choice(lines).strip(), random.choice(lines).strip() 


def is_primitive_root(g, p):
    required = set()
    for i in range(1, p):
        required.add(pow(g, i, p))
    return len(required) == p - 1

def generate_random_number_dh(path: str):
    with open(path, 'r') as file:
        lignes = file.readlines()
        nombres = [int(l.strip()) for l in lignes if l.strip().isdigit()]
    
    petits_p = [n for n in nombres if n < 5000]

    if not petits_p:
        raise ValueError("Aucun nombre premier < 5000 dans le fichier.")

    while True:
        p = random.choice(petits_p)
        racines_possibles = [g for g in range(2, p) if is_primitive_root(g, p)]
        if racines_possibles:
            g = random.choice(racines_possibles)
            return p, g

    


# ========== ENVOI ==========
def byte_to_string(message: bytes):
    return message.decode('utf-8', errors='ignore')

def str_to_int_list(message: str) -> list[int]:
    return [int.from_bytes(c.encode(), 'big') for c in message]

def int_list_to_bytes(ints: list[int]) -> bytes:
    return b''.join([i.to_bytes(4, 'big') for i in ints])

def wrap_message(ints: list[int], marker: bytes = b's') -> bytes:
    prefix = b'ISC'
    length = len(ints).to_bytes(2, 'big')
    message_bytes = int_list_to_bytes(ints)
    return prefix + marker + length + message_bytes

def prepare_message(msg: str, marker: bytes = b's') -> bytes:
    return wrap_message(str_to_int_list(msg), marker)


# ========== RÉCEPTION ==========

def unwrap_message(data: bytes) -> str:
    """Nettoie et décode une réponse brute du serveur."""
    try:
        reponse = data.decode('utf-8', errors='ignore').strip().replace('\x00', '')
        if reponse.startswith("ISCs") or reponse.startswith("ISCt"):
            reponse = reponse[5:]
        return reponse
    except Exception as e:
        print(f"[Erreur de décodage] : {e}")
        return ""


# ========== ENVOI/RÉCEPTION SOCKET ==========

def send(sock: socket.socket, msg: bytes):
    """Envoie un message binaire au serveur."""
    try:
        sock.send(msg)
    except Exception as e:
        print(f"[Erreur d’envoi] : {e}")

def receive(sock: socket.socket) -> str:
    """Récupère une réponse propre depuis le serveur."""
    try:
        data = sock.recv(1024)
        return unwrap_message(data)
    except Exception as e:
        print(f"[Erreur de réception] : {e}")
        return ""

# ========================
# Chrono
# ========================


def chrono(label, func, *args, **kwargs):
    print(f"▶️ Début : {label}")
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    print(f"⏱️ {label} terminé en {end - start:.4f} secondes\n")
    return result