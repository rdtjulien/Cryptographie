import socket
import math
import protocol
import rsa

# ========================
# Test RSA local (hors serveur)
# ========================

def test_rsa_local():
    print("=== Test RSA local (chiffrement / déchiffrement sans serveur) ===")
    
    message = "RSA test message"

    # Génère deux nombres premiers et une clé RSA
    p, q = protocol.get_random_primes()
    n, e, d = rsa.generate_key(p, q)

    # Chiffre le message avec la clé publique
    encrypted = encode_RSA(message, e, n)

    # Déchiffre avec la clé privée
    decrypted_chars = [chr(pow(c, d, n)) for c in encrypted]
    decrypted_message = ''.join(decrypted_chars)

    print("Message original  :", message)
    print("Message chiffré   :", encrypted)
    print("Message déchiffré :", decrypted_message)

    assert decrypted_message == message, "❌ Le message déchiffré ne correspond pas au message original !"
    print("✅ Test RSA local réussi.\n")

def encode_RSA(message: str, e, n):
    return [pow(int.from_bytes(char.encode(), 'big'), int(e), int(n)) for char in message]


# ========================
# Test communication socket
# ========================

def test_protocol_communication():
    print("=== Test communication socket interne ===")
    s1, s2 = socket.socketpair()
    test_message = "Hello, crypto!"
    
    to_send = protocol.prepare_message(test_message)
    protocol.send(s1, to_send)

    received_raw = s2.recv(1024)
    clean_msg = protocol.unwrap_message(received_raw)

    print(f"Message original : {test_message}")
    print(f"Message reçu     : {clean_msg}")
    assert clean_msg == test_message, "❌ Le message reçu ne correspond pas au message envoyé !"
    print("✅ Test de communication réussi.\n")

# ========================
# Test pipeline de conversion
# ========================

def test_conversion_pipeline():
    print("=== Test pipeline de conversion ===")
    test_msg = "Test123"
    int_list = protocol.str_to_int_list(test_msg)
    byte_result = protocol.int_list_to_bytes(int_list)

    print("String d'origine :", test_msg)
    print("Liste d'int      :", int_list)
    print("Bytes            :", byte_result)
    print("✅ Pipeline conversion fonctionnelle.\n")

# ========================
# Lancement
# ========================

if __name__ == "__main__":
    test_protocol_communication()
    test_conversion_pipeline()
    test_rsa_local()
