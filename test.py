a = "tést"

a = a.encode('utf-8')
temp = []
for i in a:
    temp.append(i.to_bytes(4, 'big'))

print(temp)
