
def validar_entrada(mensaje, tipo):
    while True:
        entrada = input(mensaje)
        if entrada.lower() == 's':
            return 's'
        if tipo == "num":
            try:
                valor = int(entrada)
                return valor
            except ValueError:
                print("Por favor, ingrese un número válido.")
        else:
            return entrada

def crear_y_modificar_matriz():
    print("\n-------------------------")
    print("| Generador de Matrices |")
    print("-------------------------")

    columnas, filas  = validar_entrada("\nIngrese de cuantas columnas quiere la matriz: ", "num"), validar_entrada("Ingrese de cuantas filas quiere la Matriz: ", "num")
    
    matriz = [[0]* columnas for _ in range(filas)]
    
    print("\n----------------------------------")
    print(f"| La matriz ingresada es de {filas}x{columnas}: |")
    print("----------------------------------\n")

    for fila in matriz:
        print(fila)
    print()
    

    while True:
        fila = validar_entrada("Ingrese la fila de la posición que desea modificar (si desea salir coloque s): ", "num")
        if fila == 's':
            break
        columna = validar_entrada("Ingrese la columna de la posición que desea modificar: ", "num")
        if columna == 's':
            break

        if fila < len(matriz) and columna < len(matriz[0]):
            valor = validar_entrada(f"Ingrese el valor para la posición [{fila}][{columna}]: ", "num")
            if valor == 's':
                break
            matriz[fila][columna] = valor
            print(" ")
            for fila in matriz:
                print(fila)
            print(" ")
        else:
            print("\n  -POSICION FUERA DE RANGO, por favor intente nuevamente.\n")
            
while True:

    crear_y_modificar_matriz()
    otra = input("¿Desea crear otra matriz? (s/n): ")
    if otra.lower() != 's': 
        print("Gracias por utilizar el generador de Matrices. Adios..\n")
        break

