import socket
import protocol
import rsa

# ========================
# Connexion au serveur
# ========================

def create_socket():
    """Crée et connecte un socket au serveur distant"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(("vlbelintrocrypto.hevs.ch", 6000))
        print("✅ Connecté au serveur.")
        return sock
    except Exception as e:
        print(f"❌ Impossible de se connecter : {e}")
        return None

# ========================
# Préparation du message RSA
# ========================

def get_rsa_encoded_message():
    """
    Construit la commande à envoyer au serveur
    Format attendu : task RSA encode <longueur du message attendu par le serveur>
    """
    task_message = "task RSA encode 16"
    return protocol.prepare_message(task_message)

# ========================
# Test complet RSA serveur
# ========================

def test_rsa_server():
    print("=== Test RSA avec serveur réel ===")
    sock = create_socket()
    if not sock:
        return

    try:
        # Prépare et lance l'envoi RSA (module rsa.py)
        msg = get_rsa_encoded_message()
        rsa.encrypt(sock, protocol.receive, msg)
        print("✅ Test RSA avec serveur terminé.\n")

    except Exception as e:
        print(f"❌ Erreur durant le test RSA serveur : {e}")

    finally:
        sock.close()

# ========================
# Lancement
# ========================

if __name__ == "__main__":
    test_rsa_server()
