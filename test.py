message1 = "hello worldé"
message1 = list(message1)
encode = []
temp = ""

for i in message1:
    temp = i.encode('utf-8')
    encode.append(temp)
message1 = encode 

     
tim = 0
recode = []

for i in message1:
    tim = int.from_bytes(i, 'big')
    c = tim.to_bytes(4,'big')
    recode.append(c)

r = []
x = 0
for i in recode:
    x = int.from_bytes(i, 'big')
    r.append(x)

print(r)

temp = []
for i in r:
    z = i.to_bytes(4,'big')
    temp.append(z)
r = temp

new_message = ""
for i in r:
    new_message += str(i)
print(new_message)