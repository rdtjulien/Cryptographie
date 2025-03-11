import send_message

def vigenere_encrypt_ascii(text, key):
    encrypted_text = []
    key_length = len(key)
    
    for i, char in enumerate(text):
        char_code = ord(char)
        
        if 32 <= char_code <= 126:
            shift = ord(key[i % key_length]) % 95
            new_char = chr(((char_code - 32 + shift) % 95) + 32)
        else:
            new_char = char

        encrypted_text.append(new_char)

    return ''.join(encrypted_text)

def vigenere_decrypt_ascii(text, key):
    decrypted_text = []
    key_length = len(key)
    
    for i, char in enumerate(text):
        char_code = ord(char)
        
        if 32 <= char_code <= 126:
            shift = ord(key[i % key_length]) % 95
            new_char = chr(((char_code - 32 - shift) % 95) + 32)
        else:
            new_char = char

        decrypted_text.append(new_char)

    return ''.join(decrypted_text)


def encode(sock, reponse_func, encoded_message):
        sock.send(encoded_message)

        x = reponse_func()
        key = x.split()
        key = key[len(key)-1]
        text = reponse_func()
        
        encoded_message = vigenere_decrypt_ascii(text, key)

        print(f"Vigenere message: {encoded_message}")

        encoded_message = send_message.encode_message(b's', encoded_message)
        sock.send(encoded_message)
        reponse_func()



