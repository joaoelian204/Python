import sqlite3

#============================== Conexion a la base de datos 'cartelera' ============================

# Nombre del archivo de la base de datos SQLite
DB_FILE = 'cartelera.db'

# Función para conectar a la base de datos SQLite
def conectar_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    return conn, cursor

# Función para cerrar la conexión a la base de datos SQLite
def cerrar_db(conn):
    if conn:
        conn.close()
        
#====================================== Crear tablas en la base de datos 'cartelera' ==================================

# Función para crear la tabla 'peliculas' si no existe
def crear_tabla_peliculas():
    conn, cursor = conectar_db()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS peliculas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            genero TEXT,
            duracion INTEGER,
            sinopsis TEXT,
            imagen TEXT
        )
    ''')
    conn.commit()
    cerrar_db(conn)

# Función para crear la tabla 'reservas' si no existe
def crear_tabla_reservas():
    conn, cursor = conectar_db()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER,
            id_pelicula INTEGER,
            hora TEXT,
            sala TEXT,
            asiento TEXT,
            FOREIGN KEY (id_usuario) REFERENCES usuarios (id),
            FOREIGN KEY (id_pelicula) REFERENCES peliculas (id)
        )
    ''')
    conn.commit()
    cerrar_db(conn)

# Función para crear la tabla 'horarios' si no existe
def crear_tabla_horarios():
    conn, cursor = conectar_db()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS horarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pelicula INTEGER,
            horario TEXT,
            sala TEXT,
            FOREIGN KEY (id_pelicula) REFERENCES peliculas (id)
        )
    ''')
    conn.commit()
    cerrar_db(conn)

# Función para insertar un horario en la tabla 'horarios'
def insertar_horario(id_pelicula, horario, sala):
    conn, cursor = conectar_db()
    cursor.execute('''
        INSERT INTO horarios (id_pelicula, horario, sala)
        VALUES (?, ?, ?)
    ''', (id_pelicula, horario, sala))
    conn.commit()
    cerrar_db(conn)


    
#============================ Funciones para manipular la base de datos 'cartelera' ================================

# Función para cargar todos los horarios de una película específica
def cargar_horarios_pelicula(id_pelicula):
    conn, cursor = conectar_db()
    cursor.execute('''
        SELECT id, id_pelicula, horario, sala
        FROM horarios
        WHERE id_pelicula = ?
    ''', (id_pelicula,))
    horarios = cursor.fetchall()
    cerrar_db(conn)
    return horarios

# Función para actualizar un horario existente
def actualizar_horario(id_horario, nuevo_horario, nueva_sala):
    conn, cursor = conectar_db()
    cursor.execute('UPDATE horarios SET horario=?, sala=? WHERE id=?', (nuevo_horario, nueva_sala, id_horario))
    conn.commit()
    cerrar_db(conn)

# Función para eliminar un horario específico por su ID
def eliminar_horario(id_horario):
    conn, cursor = conectar_db()
    cursor.execute('DELETE FROM horarios WHERE id=?', (id_horario,))
    conn.commit()
    cerrar_db(conn)

# Función para eliminar todos los horarios asociados a una película por su ID
def eliminar_horarios_por_pelicula(id_pelicula):
    conn, cursor = conectar_db()
    cursor.execute('DELETE FROM horarios WHERE id_pelicula=?', (id_pelicula,))
    conn.commit()
    cerrar_db(conn)

# Función para eliminar salas asociadas a un horario específico (opcionalmente con un cursor proporcionado)
def eliminar_salas_por_horario(id_horario, cursor=None):
    close_conn_after = False
    if cursor is None:
        conn, cursor = conectar_db()
        close_conn_after = True
    
    cursor.execute('DELETE FROM salas WHERE id_horario=?', (id_horario,))
    
    if close_conn_after:
        conn.commit()
        cerrar_db(conn)

# Función para eliminar una película por su ID
def eliminar_pelicula(id_pelicula):
    conn, cursor = conectar_db()
    
    # Eliminar primero los horarios asociados a la película
    eliminar_horarios_por_pelicula(id_pelicula)
    
    # Luego eliminar la película en sí
    cursor.execute('DELETE FROM peliculas WHERE id=?', (id_pelicula,))
    conn.commit()
    cerrar_db(conn)

# Función para cargar todas las películas de la base de datos
def cargar_cartelera():
    conn, cursor = conectar_db()
    cursor.execute('SELECT id, titulo, genero, duracion, sinopsis, imagen FROM peliculas')
    peliculas = cursor.fetchall()
    cerrar_db(conn)
    return peliculas

# Función para insertar una nueva película en la base de datos
def insertar_pelicula(titulo, genero, duracion, sinopsis, imagen):
    conn, cursor = conectar_db()
    cursor.execute('''
        INSERT INTO peliculas (titulo, genero, duracion, sinopsis, imagen)
        VALUES (?, ?, ?, ?, ?)
    ''', (titulo, genero, duracion, sinopsis, imagen))
    conn.commit()
    id_pelicula = cursor.lastrowid
    cerrar_db(conn)
    return id_pelicula

# Función para seleccionar un horario específico por su ID
def seleccionar_horario(id_horario):
    conn, cursor = conectar_db()
    cursor.execute('SELECT id, id_pelicula, horario, sala FROM horarios WHERE id=?', (id_horario,))
    horario = cursor.fetchone()
    cerrar_db(conn)
    return horario

# Función para actualizar los datos de una película existente
def actualizar_pelicula(id_pelicula, titulo, genero, duracion, sinopsis, imagen):
    conn, cursor = conectar_db()
    cursor.execute('''
        UPDATE peliculas
        SET titulo=?, genero=?, duracion=?, sinopsis=?, imagen=?
        WHERE id=?
    ''', (titulo, genero, duracion, sinopsis, imagen, id_pelicula))
    conn.commit()
    cerrar_db(conn)

# Función para seleccionar una película específica por su ID
def seleccionar_pelicula(id_pelicula):
    conn, cursor = conectar_db()
    cursor.execute('SELECT id, titulo, genero, duracion, sinopsis, imagen FROM peliculas WHERE id=?', (id_pelicula,))
    pelicula = cursor.fetchone()
    cerrar_db(conn)
    return pelicula



