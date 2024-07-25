from Actividad_Clases.validar import validar_entrada

while True:
    print("\n-------------------------")
    print("| Generador de Matrices |")
    print("-------------------------")

    columnas = validar_entrada("\nIngrese de cuántas columnas quiere la matriz: ", "num")
    filas = validar_entrada("Ingrese de cuántas filas quiere la matriz: ", "num")

    matriz = [[0 for _ in range(columnas)] for _ in range(filas)]
    print("\n----------------------------------")
    print(f"| La matriz ingresada es de {filas}x{columnas}: |")
    print("----------------------------------\n")


    for fila in matriz:
        fila.append(100)
        fila.insert(0, 100)
        
    matriz.append([100 for _ in range(columnas + 2)])
    matriz.insert(0, [100 for _ in range(columnas + 2)])
    print("\nMatriz actualizada:")
    print(matriz)


    for fila in matriz:
        print(fila)
    print()

    while True:
        fila_input = input("Ingrese la fila de la posición que desea modificar (si desea salir coloque s ): ").strip()
        if fila_input.lower() == 's':
            break

        fila = validar_entrada(fila_input, "num")
        fila = int(fila)

        columna_input = input("Ingrese la columna de la posición que desea modificar: ").strip()
        columna = validar_entrada(columna_input, "num")
        columna = int(columna)

        if 0 <= fila < len(matriz) and 0 <= columna < len(matriz[0]):
            valor_input = input(f"Ingrese el valor para la posición [{fila}][{columna}]: ").strip()
            valor = validar_entrada(valor_input, "num")
            valor = int(valor)
            matriz[fila][columna] = valor
            print("\nMatriz actualizada:")
            for fila in matriz:
                print(fila)
            print()
        else:
            print("\nPosición fuera de rango, por favor intente nuevamente.")

    otra = input("¿Desea crear otra matriz? (si/no): ").strip().lower()
    if otra != 'si':
        print("Fin de la ejecución.")
        break
