import sqlite3

# Conectar a la base de datos (se creará si no existe)
conn = sqlite3.connect('profesores.db')
cursor = conn.cursor()

# Eliminar la tabla si existe (opcional, para limpiar la base de datos)
cursor.execute('DROP TABLE IF EXISTS usuarios')

# Crear la tabla de usuarios de nuevo
cursor.execute('''
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY,
    usuario TEXT,
    contrasena TEXT
)
''')

# Lista de ProfesoresUsuarios
LisProfesores = [
    {"usuario": "Jose", "contraseña": "1234"},
    {"usuario": "Maria", "contraseña": "123"},
    {"usuario": "Pedro", "contraseña": "12345"}
]

def insertar_profesor(profesor):
    cursor.execute('''INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)''', (profesor['usuario'], profesor['contraseña']))
    conn.commit()

# Insertar los profesores iniciales en la base de datos
for profesor in LisProfesores:
    insertar_profesor(profesor)

# Lista de estudiantes
LisEstudiantes = []

# Función para registrar un profesor
def registrar_profesor():
    print("\n=== Registro de Profesor ===")
    usuario = input('Ingrese el usuario: ')
    contraseña = input('Ingrese la contraseña: ')
    nuevo_profesor = {"usuario": usuario, "contraseña": contraseña}
    LisProfesores.append(nuevo_profesor)
    insertar_profesor(nuevo_profesor)
    print("Profesor registrado correctamente.")

# Función para mostrar el menú principal
def mostrar_menu_principal():
    print("\n======================")
    print("=  Gestor de Estudiantes  =")
    print("======================")
    print("1. Iniciar sesión")
    print("2. Registrarte")
    print("======================")
    opcion = input('Seleccione una opción: ')
    return opcion

# Función para iniciar sesión
def login():
    print("\n=== Bienvenido al Gestor de Estudiantes ===")
    while True:
        opcion = mostrar_menu_principal()
        
        if opcion == '1':
            print("\n=== Iniciar Sesión ===")
            usuario = input('Ingrese el usuario: ')
            contraseña = input('Ingrese la contraseña: ')
            cursor.execute('''SELECT * FROM usuarios WHERE usuario=? AND contrasena=?''', (usuario, contraseña))
            if cursor.fetchone():
                print(f'\nBienvenido, Profesor {usuario}!')
                menu()
                return True
            else:
                print('Usuario o contraseña incorrectos')
        elif opcion == '2':
            registrar_profesor()
        else:
            print("Opción no válida")

# Función para mostrar el menú
def menu():
    while True:
        print("\n=== Menú Principal ===")
        opciones = ["Agregar Estudiante", "Imprimir Lista de Estudiantes", "Buscar Estudiantes", "Cerrar Sesión"]
        for i, opcion in enumerate(opciones, 1):
            print(f"{i}. {opcion}")
        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            agregar_estudiante()
        elif opcion == '2':
            imprimir_lista()
        elif opcion == '3':
            buscar_estudiantes()
        elif opcion == '4':
            print("Sesión cerrada. ¡Hasta luego!")
            break
        else:
            print("Opción no válida, intente de nuevo.")

# Función para agregar un estudiante
def agregar_estudiante():
    print("\n=== Agregar Estudiante ===")
    repetir = int(input('¿Cuántos estudiantes desea agregar?: '))
    for i in range(repetir):
        NombreEstudiante = input('Ingrese el nombre del estudiante: ')
        LisEstudiantes.append(NombreEstudiante)
    print("Estudiantes agregados correctamente.")

# Función para imprimir la lista de estudiantes
def imprimir_lista():
    print("\n=== Lista de Estudiantes ===")
    for estudiante in LisEstudiantes:
        print(estudiante)

# Función para buscar un estudiante
def buscar_estudiantes():
    print("\n=== Buscar Estudiante ===")
    nombre_buscar = input('Ingrese el nombre del estudiante a buscar: ')
    encontrados = [estudiante for estudiante in LisEstudiantes if estudiante == nombre_buscar]
    if encontrados:
        print(f'Estudiantes encontrados: {", ".join(encontrados)}')
    else:
        print("Estudiante no encontrado.")

# Inicio del programa
login()
conn.commit()
conn.close()



