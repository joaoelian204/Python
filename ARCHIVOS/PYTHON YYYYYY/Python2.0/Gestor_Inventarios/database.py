import sqlite3

# Conexión a la base de datos SQLite
conexion = sqlite3.connect("GestorDeInventario.db")
cursorBD = conexion.cursor()

# Crear tablas si no existen
cursorBD.execute('''
CREATE TABLE IF NOT EXISTS PRODUCTO (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NOMBRE TEXT NOT NULL,
    CATEGORIA TEXT NOT NULL
)
''')

cursorBD.execute('''
CREATE TABLE IF NOT EXISTS HISTORIAL_BORRADOS (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NOMBRE TEXT NOT NULL,
    CATEGORIA TEXT NOT NULL,
    FECHA_ELIMINACION TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Funciones de base de datos
def mostrar_productos_db():
    cursorBD.execute("SELECT * FROM PRODUCTO")
    return cursorBD.fetchall()

def insertar_producto_db(nombre, categoria):
    cursorBD.execute('''INSERT INTO PRODUCTO (NOMBRE, CATEGORIA) VALUES (?, ?)''', (nombre, categoria))
    conexion.commit()

def seleccionar_productos_db():
    cursorBD.execute('''SELECT * FROM PRODUCTO''')
    return cursorBD.fetchall()

def actualizar_producto_db(id_producto, diccionario):
    valores_validos = ['NOMBRE', 'CATEGORIA']
    for key, value in diccionario.items():
        if key not in valores_validos:
            raise Exception('Esa columna no existe')
        else:
            query = '''UPDATE PRODUCTO SET {} = ? WHERE ID = ?'''.format(key)
            cursorBD.execute(query, (value, id_producto))
    conexion.commit()

def eliminar_producto_db(id_producto):
    cursorBD.execute("SELECT * FROM PRODUCTO WHERE ID = ?", (id_producto,))
    producto = cursorBD.fetchone()
    if producto:
        cursorBD.execute('''INSERT INTO HISTORIAL_BORRADOS (NOMBRE, CATEGORIA) VALUES (?, ?)''', (producto[1], producto[2]))
        cursorBD.execute('''DELETE FROM PRODUCTO WHERE ID = ?''', (id_producto,))
        conexion.commit()
    else:
        print("Producto no encontrado.")

def mostrar_todos_los_eliminados_db():
    cursorBD.execute("SELECT * FROM HISTORIAL_BORRADOS")
    return cursorBD.fetchall()

def close_db():
    conexion.close()
