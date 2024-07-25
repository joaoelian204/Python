# Lista inicial
lista = [1, 2, 3, 4, 5]
# Lista para almacenar elementos borrados
historial_borrados = []

def eliminar_elemento(lista, historial_borrados, elemento):
    if elemento in lista:
        lista.remove(elemento)
        historial_borrados.append(elemento)

# Eliminar elementos
eliminar_elemento(lista, historial_borrados, 1)
eliminar_elemento(lista, historial_borrados, 5)

print("Elementos en la lista:", lista)
print("Historial de borrados:", historial_borrados)
