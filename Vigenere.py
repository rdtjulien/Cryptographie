def vigenere_encrypt_ascii(text, key):
    encrypted_text = []
    key_length = len(key)
    
    for i, char in enumerate(text):
        char_code = ord(char)
        
        if 32 <= char_code <= 126:  # Seulement les caractères imprimables
            shift = ord(key[i % key_length]) % 95  # Décalage basé sur la clé
            new_char = chr(((char_code - 32 + shift) % 95) + 32)  # Modulo 95 pour rester dans la plage ASCII imprimable
        else:
            new_char = char  # Garder les caractères non imprimables intacts

        encrypted_text.append(new_char)

    return ''.join(encrypted_text)

def vigenere_decrypt_ascii(text, key):
    decrypted_text = []
    key_length = len(key)
    
    for i, char in enumerate(text):
        char_code = ord(char)
        
        if 32 <= char_code <= 126:  # Seulement les caractères imprimables
            shift = ord(key[i % key_length]) % 95
            new_char = chr(((char_code - 32 - shift) % 95) + 32)  # On soustrait le décalage pour déchiffrer
        else:
            new_char = char

        decrypted_text.append(new_char)

    return ''.join(decrypted_text)

# Exemple d'utilisation
message = "Hello, World! 1234 @$#"
cle = "MyKey"

texte_chiffre = vigenere_encrypt_ascii(message, cle)
print("Chiffré :", texte_chiffre)

texte_dechiffre = vigenere_decrypt_ascii(texte_chiffre, cle)
print("Déchiffré :", texte_dechiffre)
