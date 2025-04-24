import socket
import random

# ========= Données communes =========

file_path = "nombres_premiers.txt"       

def generate_random_number(path: str):
    with open(path, 'r') as file: 
        lines = file.readlines()   
    return random.choice(lines).strip(), random.choice(lines).strip() 
    
print(generate_random_number(file_path))
    


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
