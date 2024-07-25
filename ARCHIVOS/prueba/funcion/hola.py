# funcion/hola.py

def calcular_asientos_ocupados(matriz_asientos):
    asientos_ocupados = sum(sum(fila) for fila in matriz_asientos)
    return asientos_ocupados

def calcular_asientos_desocupados(matriz_asientos):
    total_asientos = len(matriz_asientos) * len(matriz_asientos[0])  # Total de asientos en la matriz
    asientos_ocupados = calcular_asientos_ocupados(matriz_asientos)
    asientos_desocupados = total_asientos - asientos_ocupados
    return asientos_desocupados
