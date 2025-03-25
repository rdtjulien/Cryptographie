def decode_RSA(encoded_list, d, n):
    decoded_chars = [pow(c, d, n) for c in encoded_list]  # Décryptage RSA
    decoded_message = ''.join(bytes([m]).decode() for m in decoded_chars)  # Conversion en texte
    return decoded_message

# Paramètres donnés
n = 9845984
e = 9023483

# Facteurs premiers de n (trouvés précédemment)
p, q = 2, 4923992

# Calcul de φ(n)
phi_n = (p - 1) * (q - 1)

# Calcul de d (inverse modulaire de e mod φ(n))
d = pow(e, -1, phi_n)

# Message chiffré (fourni sous forme de chaîne de caractères)
code = "8ڠ`c►2ic↨&`K"

# Convertir le texte chiffré en une liste de nombres Unicode
encoded_list = [ord(c) for c in code]

# Décodage du message
decoded_message = decode_RSA(encoded_list, d, n)

print("Message déchiffré:", decoded_message)
