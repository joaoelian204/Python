import sqlite3

def crear_tabla_productos():
    conn = sqlite3.connect('cartelera.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio REAL NOT NULL,
            imagen TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Llamar a la función para crear la tabla
crear_tabla_productos()
