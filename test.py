message1 = "hello worldé"
message1 = list(message1)
encode = []
temp = ""

for i in message1:
    temp = i.encode('utf-8')
    encode.append(temp)
message1 = encode 
print(message1)

     
tim = 0
recode = []

for i in message1:
    tim = int.from_bytes(i, 'big')
    c = tim.to_bytes(4,'big')
    recode.append(c)

print(recode)

