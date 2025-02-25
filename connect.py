import socket

HEADER = "ISC"
test = ''
PORT = 6000
ADDRESS = 'vlbelintrocrypto.hevs.ch'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((ADDRESS, PORT))
except Exception as e:
    print("Cannot connect to the server:", e)
print("Connected")

bytes_isc = bytes(HEADER, 'utf-8')
print(bytes_isc)

message = 'task shift encode 6'
length_string = int(len(message))
bytes_val = length_string.to_bytes(2,'big')

message = f'{bytes_isc}t{bytes_val}{message}'

print(f"message: {message}")
sock.send(message.encode('utf-8'))

reponse = sock.recv(1024)
print(f"réponse: {reponse.decode('utf-8')}")

sock.close()
#print(bytes(message.encode()))
