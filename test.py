message1 = "hello worldé"
message1 = list(message1)
encode = []
temp = ""

for i in message1:
    temp = i.encode('utf-8')
    encode.append(temp)
print(encode)