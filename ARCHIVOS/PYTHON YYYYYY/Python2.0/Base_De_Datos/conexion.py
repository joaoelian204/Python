import sqlite3

# Conexión a la base de datos SQLite
conexion = sqlite3.connect("GestorDeInventario")
cursorBD = conexion.cursor()


def mostrarProductos():
    cursorBD.execute("SELECT * FROM PRODUCTO")
    productos = cursorBD.fetchall()
    for producto in productos:
        print(producto)

def insertarProducto(nombre, precio):
    cursorBD.execute('''INSERT INTO PRODUCTO (NOMBRE, PRECIO) VALUES (?, ?)''', (nombre, precio))
    conexion.commit()

def seleccionarProductos():
    cursorBD.execute('''SELECT * FROM PRODUCTO''')
    lista = cursorBD.fetchall()
    return lista

def actualizarProducto(codigo, diccionario):
    valoresValidos = ['NOMBRE', 'PRECIO']
    for key, value in diccionario.items():
        if key not in valoresValidos:
            raise Exception('Esa columna no existe')
        else:
            query = '''UPDATE PRODUCTO SET {} = ? WHERE CODIGO = ?'''.format(key)
            cursorBD.execute(query, (value, codigo))
    conexion.commit()

def eliminarProducto(codigo):
    cursorBD.execute('''DELETE FROM PRODUCTO WHERE CODIGO = ?''', (codigo,))
    conexion.commit()




# Seleccionar y mostrar todos los productos después de las operaciones
print(*seleccionarProductos())



conexion.close()


