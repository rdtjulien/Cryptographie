def byte_message(message: str):
    new_message = []
    for i in message:
        new_message.append(ord(i).to_bytes(4,'big'))

    return b''.join(new_message)

def encode_message(m:bytes, message: str):
    prefix = b'ISC'
    length = len(message).to_bytes(2, 'big')
    new_message = byte_message(message)

    return prefix + m + length + new_message


<<<<<<< HEAD
#pyuic5 -x test.ui -o test.py
=======
#pyuic5 -x GUI_crypto_V3.ui -o GUI.py
>>>>>>> 2db07dd56caf78cc8c3be64984e787b991733bbe
#git reset --hard HEAD^