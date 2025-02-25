import socket

PORT = 6000
ADDRESS = 'vlbelintrocrypto.hevs.ch'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((ADDRESS, PORT))
except Exception as e:
    print("Cannot connect to the server:", e)
print("Connected")

message1 = "hello worldé"
message1 = list(message1)
print(message1)


message = 'task shift encode 6'
length_string = int(len(message))
bytes_val = length_string.to_bytes(2,'big')

message = f'ISCs000500000048000000650000006C0000006C0000006F'

print(f"message: {message}")
sock.send(message.encode('utf-8'))

reponse = sock.recv(1024)
print(f"réponse: {reponse.decode()}")

sock.close()
#print(bytes(message.encode()))


