#Crear una matriz
def crear_matriz(filas, columnas):
    matriz = []
    for i in range(filas):
        matriz.append([0]*columnas)
    return matriz

def imprimir_matriz(matriz):
    for i in range(len(matriz)):
        print(matriz[i])
        
def llenar_matriz(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            matriz[i][j] = int(input("Ingrese un número: "))
    return matriz

def sumar_matriz(matriz):
    suma = 0
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            suma += matriz[i][j]
    return suma

def main():
    filas = int(input("Ingrese el número de filas: "))
    columnas = int(input("Ingrese el número de columnas: "))
    matriz = crear_matriz(filas, columnas)
    matriz = llenar_matriz(matriz)
    imprimir_matriz(matriz)
    print("La suma de la matriz es: ", sumar_matriz(matriz))
    
main()
