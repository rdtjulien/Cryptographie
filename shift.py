#définir taille du message + Hex
def taille_message(message: str):
    length_string = int(len(message))
    bytes_val = length_string.to_bytes(2,'big')
    bytes_val = bytes_val.hex().upper()
    print(f"LongueurMessageHex : \n{bytes_val}")
    return bytes_val

#transforme en byte char by char
def byte_to_char(message1: str):
    temp = []
    encode = ""

    message1 = list(message1)
    for i in message1:
        encode = i.encode('utf-8')
        temp.append(encode)
    print(f"transfoChar : \n{temp}")
    temp
    return temp

#transformer en Int
def trans_to_int(message1: str):
    list_to_int = 0
    modif_message = []

    for i in message1:
        list_to_int = int.from_bytes(i,'big')
        modif_message.append(list_to_int)
    print(f"ListInt : \n{modif_message}")
    return modif_message

#faire les manipulations sur les INT
def manip_int(message1):
    temp = []
    k = 0

    for i in message1:
        x = i + k
        temp.append(x)
    print(f"ManipInt : \n{temp}")
    return temp

#re transformer en Byte
def re_trans_to_byte(message1: str):
    temp = []
    for i in message1:
        c = i.to_bytes(4,'big')
        temp.append(c)
    print(f"ReTransfoByte : \n{temp}")    
    return temp

#Transfo en Hex pour le bon format de transmission
def trans_byte_to_hex(message1: str):
    full_data = b''.join(message1)
    message1 = full_data.hex().upper()
    print(f"trandsfoByteToHex : \n{message1}")
    return message1

#mettre en forme le message et transmettre (encapsuler)
def encapsulation(isc, m, bytes_val, message):
    message_trans = f'{isc}{m}{bytes_val}{message}'
    print(f"message: \n{message_trans}")
    return message_trans

#def response():

