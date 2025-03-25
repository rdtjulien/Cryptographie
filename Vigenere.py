import send_message

#Bricolage
def byte_message(message: str):
    new_message = []
    for i in message:
        new_message.append(i.to_bytes(4,'big'))

    return b''.join(new_message)

def encode_message_vigenere(m:bytes, message: str, length: int):
    prefix = b'ISC'
    length = length.to_bytes(2, 'big')
    new_message = byte_message(message)

    return prefix + m + length + new_message

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

def encode(sock, reponse_func, encoded_message):
    sock.send(encoded_message)
    k = reponse_func()
    k = get_key(k)
    serv_reponse = reponse_func()
    vigenere_message = encrypt_vigenere(serv_reponse, k)
    print(f"Vigenere message: {vigenere_message}")
    vigenere_message = encode_message_vigenere(b's', vigenere_message, 10)
    sock.send(vigenere_message)
    serv_reponse = reponse_func()