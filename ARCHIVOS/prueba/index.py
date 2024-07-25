# index.py

from funcion.hola import *

# Ejemplo de uso en otro proyecto
matriz_asientos = [
    [0, 1, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0],
]

# Llama a las funciones importadas
asientos_ocupados = calcular_asientos_ocupados(matriz_asientos)
asientos_desocupados = calcular_asientos_desocupados(matriz_asientos)

# Imprime los resultados
print(f"Asientos Ocupados: {asientos_ocupados}")
print(f"Asientos Desocupados: {asientos_desocupados}")






