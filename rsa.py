serv = "You are asked to encode the text in the following message with the key n=1399596323, e=2760739"
serv_mes = "es feuilles dentées"

number = serv
mod = number.split('=')
n = mod[1]
n = n[:-3]
e = mod[2]


print(f"n = {n}")
print(f"e = {e}")

text = serv_mes.encode('utf-8')
text = text.decode('utf-8')
print(text)
temp = []
for i in text:
    i = ord(i)
    i = (i**int(e)) % int(n)
    temp.append(int(i))
print(temp)

#changer ord() 
#changer l'algo de calc puissance 
    