def byte_message(message: str):
    new_message = []
    for i in message:
        new_message.append(i.to_bytes(4,'big'))

    return b''.join(new_message)

def encode_message(m:bytes, message: str):
    prefix = b'ISC'
    length = len(message).to_bytes(2, 'big')
    new_message = byte_message(message)

    return prefix + m + length + new_message

def message_to_int(m: str):
    temp = []
    for i in m:
        i = i.encode()
        i = int.from_bytes(i)
        temp.append(i)
    return temp

def byte_to_string(message: bytes):
    return message.decode('utf-8', errors='ignore')

#pyuic5 -x GUI_crypto_V3.ui -o GUI.py
#git reset --hard HEAD^

'''''
Ajouter dans le GUI le choix du port
'''''
