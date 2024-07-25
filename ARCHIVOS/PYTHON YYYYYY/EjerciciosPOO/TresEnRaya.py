#juego del tres en raya
def validar_entrada(mensaje, tipo):
    while True:
        entrada = input(mensaje)  # Solicita entrada al usuario.
        if entrada.lower() == 's':  # Permite salir con 's'.
            return 's'
        if tipo == "num":
            try:
                valor = int(entrada)  # Intenta convertir la entrada a número entero.
                if valor in range(3):  # Verifica que el número esté entre 0 y 2.
                    return valor
                else:
                    print("Por favor, ingrese un número entre 0 y 2.")
            except ValueError:
                print("Por favor, ingrese un número válido.")
        else:
            return entrada  # Devuelve la entrada directamente si no es un número.

def tablero_vacio():
    return [[' ']*3 for _ in range(3)]  # Crea un tablero vacío de 3x3.

def imprimir_tablero(tablero):
    for fila in tablero:
        print('|'.join(fila))  # Imprime cada fila del tablero.
        print('-'*5)  # Imprime una línea separadora.

def obtener_movimiento(tablero, fila, columna, jugador):
    if tablero[fila][columna] == ' ':
        tablero[fila][columna] = jugador  # Marca la casilla con el símbolo del jugador.
        return True
    else:
        print('Casilla ocupada, intente de nuevo')
        return False

def verificar_ganador(tablero):
    for i in range(3):
        if tablero[i][0] == tablero[i][1] == tablero[i][2] != ' ':
            return tablero[i][0]  # Verifica filas.
        if tablero[0][i] == tablero[1][i] == tablero[2][i] != ' ':
            return tablero[0][i]  # Verifica columnas.
    
    if tablero[0][0] == tablero[1][1] == tablero[2][2] != ' ':
        return tablero[0][0]  # Verifica diagonal principal.
    if tablero[0][2] == tablero[1][1] == tablero[2][0] != ' ':
        return tablero[0][2]  # Verifica diagonal secundaria.
    
    return None

def main():
    tablero = tablero_vacio()  # Inicializa un tablero vacío.
    jugador_actual = 'X'  # El jugador 'X' empieza el juego.

    while True:
        imprimir_tablero(tablero)  # Imprime el estado actual del tablero.
        print(f'Turno del jugador {jugador_actual}')
        fila, columna = None, None  # Inicializa fila y columna.

        while fila not in range(3) or columna not in range(3):
            fila = validar_entrada('Ingrese la fila (0, 1, 2): ', 'num')  # Solicita la fila.
            columna = validar_entrada('Ingrese la columna (0, 1, 2): ', 'num')  # Solicita la columna.
        
        if obtener_movimiento(tablero, fila, columna, jugador_actual):
            ganador = verificar_ganador(tablero)  # Verifica si hay un ganador.
            if ganador:
                imprimir_tablero(tablero)
                print(f'Ganador: {ganador}')
                break  # Termina el juego si hay un ganador.
            elif all(cell != ' ' for row in tablero for cell in row):
                imprimir_tablero(tablero)
                print('La partida terminó en empate')
                break  # Termina el juego si hay un empate.
            jugador_actual = 'O' if jugador_actual == 'X' else 'X'  # Cambia el turno al otro jugador.
        else:
            print('Movimiento inválido, intente de nuevo')

if __name__ == "__main__":
    main() 

























