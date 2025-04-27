import protocol
import send_message

def get_key(key:str):
    key = key.split("shift-key ")
    return key[len(key)-1]

def generate_key(msg, key):
    key = get_key(key)
    key = list(key)
    if len(msg) == len(key):
        return key
    else:
        for i in range(len(msg) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)

def encrypt_vigenere(msg: str, key: str):
    encrypted_text = []
    key = generate_key(msg, key)
    for i in range(len(msg)):
        char = msg[i].encode()
        key_char = key[i].encode()
        char = int.from_bytes(char)
        key_char = int.from_bytes(key_char)
        encrypted_char = int(char) + int(key_char)
        encrypted_text.append(encrypted_char)

    return encrypted_text

def encode(sock, encoded_message, reponse):
    protocol.send(sock, encoded_message)
    k = reponse()
    k = get_key(k)
    serv_reponse = reponse()
    print(serv_reponse)
    vigenere_message = encrypt_vigenere(serv_reponse, k)
    vigenere_message = protocol.wrap_message(vigenere_message)
    protocol.send(sock, vigenere_message)
    reponse()

def decrypt_vigenere(msg: bytes, key: str):
    decrypted_text = []
    msg_ints = [b for b in msg if b != 0]
    key = generate_key(msg_ints, key)
    
    for i in range(len(msg_ints)):
        char = msg_ints[i]
        key_char = key[i].encode()[0]
        decrypted_char = (char - key_char) % 256
        decrypted_text.append(decrypted_char)

    return bytes(decrypted_text)