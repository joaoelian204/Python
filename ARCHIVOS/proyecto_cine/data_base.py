import sqlite3

# Conectar a la base de datos (se creará si no existe)
conn = sqlite3.connect('cartelera.db')

# Crear un cursor
cursor = conn.cursor()

# Crear la tabla de películas si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS peliculas (
    id INTEGER PRIMARY KEY,
    titulo TEXT,
    genero TEXT,
    duracion TEXT,
    imagen TEXT,
    sinopsis TEXT
)
''')

# Crear la tabla de productos
cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    precio REAL NOT NULL,
    imagen TEXT NOT NULL
)
''')


# Crear la tabla de horarios si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS horarios (
    id INTEGER PRIMARY KEY,
    id_pelicula INTEGER,
    horario TEXT,
    sala TEXT,
    FOREIGN KEY (id_pelicula) REFERENCES peliculas (id)
)
''')

# Crear la tabla publicidad_peliculas si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS publicidad_peliculas (
    id INTEGER PRIMARY KEY,
    url TEXT NOT NULL
)
''')

# Crear la tabla imagenes_publicidad si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS imagenes_publicidad (
    id INTEGER PRIMARY KEY,
    url TEXT NOT NULL
)
''')


# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()



