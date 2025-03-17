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
        char = msg[i]
        key_char = key[i]
        if char.isupper() and key_char.isalpha():
            encrypted_char = chr((ord(char) + ord(key_char) - 2 * ord('A')) % 26 + ord('A'))
        elif char.islower() and key_char.isalpha():
            encrypted_char = chr((ord(char) + ord(key_char) - 2 * ord('a')) % 26 + ord('a'))
        else:
            encrypted_char = char
        encrypted_text.append(encrypted_char)

    return "".join(encrypted_text)

def encode(sock, reponse_func, encoded_message):
    sock.send(encoded_message)
    k = reponse_func()
    k = get_key(k)
    serv_reponse = reponse_func()
    vigenere_message = encrypt_vigenere(serv_reponse, k)
    print(f"Vigenere message: {vigenere_message}")
    vigenere_message = send_message.encode_message(b's', vigenere_message)
    sock.send(vigenere_message)
    serv_reponse = reponse_func()


key = "You are asked to encode the text in the following message with the shift-key CLE"
message = "LE CHIFFRE DE VIGENERE".replace(" ","")

print(get_key(key))
print(encrypt_vigenere(message,key))