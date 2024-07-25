def crear_tabla_frecuencias(datos):
    """
    Crea una tabla de frecuencias de datos agrupados sin usar Pandas.

    Args:
        datos (list of lists): Lista de listas donde cada lista interna representa una fila con la 
                             variable a agrupar en la primera posición y el valor correspondiente en la segunda.

    Returns:
        list of lists: Tabla de frecuencias con la clase, frecuencia absoluta y frecuencia relativa.
    """

    frecuencias_absolutas = {}
    frecuencias_relativas = {}
    
    # Extraer los datos de la imagen
    for fila in datos:
        clase = fila[0]
        valor_minimo = fila[1]
        valor_maximo = fila[2]
        frecuencia = fila[3]
        rango = fila[4]
        amplitud = fila[5]
        frecuencia_absoluta = frecuencia
        frecuencia_relativa = frecuencia / rango

        if clase in frecuencias_absolutas:
            frecuencias_absolutas[clase] += frecuencia_absoluta
        else:
            frecuencias_absolutas[clase] = frecuencia_absoluta

        frecuencias_relativas[clase] = frecuencia_relativa

    tabla_frecuencias = []
    for clase, frecuencia_absoluta in frecuencias_absolutas.items():
        frecuencia_relativa = frecuencias_relativas[clase]
        tabla_frecuencias.append([clase, frecuencia_absoluta, frecuencia_relativa])

    return tabla_frecuencias


# Ejemplo de uso
datos = [
    ["muestra", 11.8, 16.6, 4.8, 7.7, 30],
    ["1", 12.1, 10.2, 11.4, 9.6, 15.3, 6],
    ["2", 8.5, 13.5, 6.2, 10.4, 5.5, 2],
    ["3", 3.6, 8.3, 9.1, 2.3, 19.5, 19.5],
    ["4", 6.1, 8, 6.8, 19.5, 12.3, 17],
    ["5", 15.9, 11.7, 11.2, 7.2, 14.5, 3],
]
tabla_frecuencias = crear_tabla_frecuencias(datos)
print(tabla_frecuencias)

