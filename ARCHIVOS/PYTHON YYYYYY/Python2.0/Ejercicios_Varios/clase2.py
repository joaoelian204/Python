estudiantes = []
#validar si es numero
def insertNum(v: str) -> int:
    num = input(f"{v}: ")
    while not(num.isnumeric()):
        num = input(f"solo numero '{v}': ")
    return int(num)
print(insertNum.__annotations__)
# validar si es str
def insertStr(v : str)->str:
    num = input(f"{v}: ")
    while num.isnumeric():
        num = input(f"solo texto '{v}': ")
    return num
print(insertStr.__annotations__)

def ingresarEstuidantes():
    #numero de estudiantes
    numEstudiantes = insertNum("¿Que numero de estudiantes desea ingresar?: ")
    #arreglo / lista de estudiantes
    #Ingresa estudiantes
    for i in range(numEstudiantes):
        nom = insertStr(f"Nombre del estudiante {i+1}")
        estudiantes.append({
            "nombre" : nom
        })
def AgregarEstudiantes():
    nom = insertStr(f"Nombre del estudiante {len(estudiantes)+1}")
    estudiantes.append({
        "nombre" : nom
    })

def impreLista():
    #Lista de estudiantes
    print()
    if len(estudiantes)== 0:
        print("no existen estudiante registrado hasta el momento")
    else:
        print("Lista de estudiantes")
        for i, v in enumerate(estudiantes):
            print(f"{i+1}: {v["nombre"]}")

def buscraEstudiantes():
    buscarNom = insertStr("Nombre del estudiante a buscar")
    # buscar
    buscar = lambda b: [i for i in estudiantes if i["nombre"] == b]
    resul = buscar(buscarNom)
    # filtrar
    if len(resul) == 0:
        print("no existen estudiante registrado")
    else:
        for i, v in enumerate(resul):
            print(f"{i+1}: {v["nombre"]}")


def LisMenu():
    me = ["Ingresar Lista de Estudiantes", "Agregar Estudiante", "Imprimir lista", "Buscar Estudiantes", "Salir"]
    print("Menu 'ingresa el numero del menu'")
    for i, v in enumerate(me):
        print(f"{i+1}: {v}")
def menu():
    while True:
        LisMenu()
        num = insertNum("Ingrese opcion: ")
        if num == 1:
            print()
            ingresarEstuidantes()
            print()
        elif num == 2:
            print()
            AgregarEstudiantes()
            print()
        elif num == 3:
            print()
            impreLista()
            print()
        elif num == 4:
            print()
            buscraEstudiantes()
            print()
        elif num == 5:
            break
        else:
            print()

            print("Opcion no valida (ingrese una opcion valida)")
            menu()
menu()