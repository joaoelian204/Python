LisEstudiantes = []
# Función para mostrar el menú
def listar_menu():
    print("\nMenú: ingresa el número de la opción")
    opciones = ["Ingresar Lista de Estudiantes", "Agregar Estudiante", "Imprimir lista", "Buscar Estudiantes", "Salir"]
    for i, opcion in enumerate(opciones, 1):
        print(f"{i}. {opcion}")
# Función para validar la entrada del usuario
def validar_entrada(valor: str, tipo: str) -> str:
    while True:
        entrada = input(f"{valor}: ")
        if tipo == "num" and entrada.isdigit():
            return int(entrada)
        elif tipo == "str" and not entrada.isdigit():
            return entrada
        else:
            mensaje = "Solo se aceptan " + ("números" if tipo == "num" else "texto")
            print(f"{mensaje}, ¡{valor}! :")
# Función para ingresar una lista de estudiantes
def ingresar_Estudiantes():
    numEstudiantes = validar_entrada("¿Qué número de estudiantes desea ingresar?", "num")
    for i in range(numEstudiantes):
        nombre_estudiante = validar_entrada(f"Nombre del estudiante {i+1}", "str")
        LisEstudiantes.append({
            "Nombre": nombre_estudiante
        })
# Función para agregar un estudiante
def Agregar_Estudiante():
    nombre_estudiante = validar_entrada(f"Nombre del estudiante {len(LisEstudiantes) + 1}", "str")
    LisEstudiantes.append({
        "Nombre": nombre_estudiante
    })
# Función para imprimir la lista de estudiantes
def Imprimir_LisEstudiante():
    if not LisEstudiantes:
        print("\nAún no se ha ingresado nombres de los estudiantes.")
    else:
        print("\nLista de estudiantes ingresados: ")
        for i, estudiante in enumerate(LisEstudiantes):
            print(f"{i + 1}. {estudiante['Nombre']}")
# Función para buscar un estudiante
def Buscar_EstudianteLis():
    BuscarEstudiante = validar_entrada("Nombre del estudiante que quiere buscar: ", "str")
    # Función lambda para buscar estudiantes por nombre
    buscar = lambda b: [estudiante for estudiante in LisEstudiantes if estudiante["Nombre"] == b]
    resul = buscar(BuscarEstudiante)
    if not resul:
        print("\nNo existe estudiante registrado.")
    else:
        print("\nResultados de búsqueda:")
        for i, v in enumerate(resul, 1):
            print(f"{i}: {v['Nombre']}")
def menu():
    while True:
        listar_menu()
        opcion = validar_entrada("Ingrese opción", "num")
        if opcion == 1:
            ingresar_Estudiantes()
        elif opcion == 2:
            Agregar_Estudiante()
        elif opcion == 3:
            Imprimir_LisEstudiante()
        elif opcion == 4:
            Buscar_EstudianteLis()
        elif opcion == 5:
            break
        else:
            print("\nOpción no válida. Ingrese una opción válida.")
menu()
