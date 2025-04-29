import protocol
import random

def decrypt(sock, encoded_message, reponse_func):
    protocol.send(sock, encoded_message)
    reponse_func()

    # Clés DH locales
    p, g = protocol.generate_random_number_dh(protocol.file_path)
    a = random.randint(2, 50)

    # Envoie p, g
    msg = f"{p},{g}"
    protocol.send(sock, protocol.prepare_message(msg))
    reponse_func()

    # Reçoit moitié de clé B
    B = int(reponse_func())

    # Envoie moitié de clé A
    A = pow(int(g), int(a), int(p))
    protocol.send(sock, protocol.prepare_message(str(A)))
    reponse_func()

    # Calcule la clé partagée
    shared = pow(int(B), int(a), int(p))
    protocol.send(sock, protocol.prepare_message(str(shared)))
    reponse_func()
