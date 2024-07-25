frase = 'Hello  world  biutifol'

for i in range(len(frase.strip())):
    print(frase[i], end=" ")
    if frase[i] == 'o':
        print(f'0', end=" ")

