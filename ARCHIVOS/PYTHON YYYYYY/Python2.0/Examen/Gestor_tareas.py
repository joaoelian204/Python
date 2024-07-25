pendientes, completadas = [], [] # Lista de tareas pendientes y completadas

def validar_entrada(mensaje, tipo):
    while True:
        entrada = input(mensaje)
        if tipo == "num" and entrada.isdigit():
            return int(entrada)
        elif tipo == "str" and not entrada.isdigit():
            return entrada.title().strip()
        else:
            notificacion = f"Solo se aceptan {('números' if tipo == 'num' else 'texto')}"
            print(notificacion)
            
def agregar_tarea():
    valor = validar_entrada("Cuántas veces va a ingresar tareas: ", "num")
    for _ in range(valor):
        print("Agregando tarea\n")
        tarea = {
            "tareas": validar_entrada("Ingrese la tarea: ", "str"),
            "descripcion": validar_entrada("Ingrese la descripción de la tarea: ", "str") }
        
        print(f"\nTarea '{tarea['tareas']}' agregada correctamente.\n")
        pendientes.append(tarea)
    print("\n")

def listar_tareas():
    print("\nListando todas las tareas\n")
    for tarea in pendientes + completadas:
        estado = "Pendiente" if tarea in pendientes else "Completada"
        print(f"Tarea: {tarea['tareas']}, Descripción: {tarea['descripcion']}, Estado: {estado}")
        
def listar_tareas_por_estado():
    print("\nListando tareas pendientes\n")
    for tarea in pendientes:
        print(f"--Tarea: {tarea['tareas']}, Descripción: {tarea['descripcion']}, Estado: Pendiente")

    print("\nListando tareas completadas\n")
    for tarea in completadas:
        print(f"--Tarea: {tarea['tareas']}, Descripción: {tarea['descripcion']}, Estado: Completada")

def marcar_tarea():
    print("Marcar tareas")
    tarea_nombre = validar_entrada("Ingrese la tarea a marcar como completada: ", "str")
    for tarea in pendientes:
        if tarea["tareas"] == tarea_nombre:
            completadas.append(tarea)
            pendientes.remove(tarea)
            print(f"Tarea '{tarea_nombre}' marcada como completada.")
            return
    print(f"\nTarea '{tarea_nombre}' no encontrada.\n")

def eliminar_tarea():
    print("Eliminando tarea")
    tarea_nombre = validar_entrada("Ingrese la tarea a eliminar: ", "str")
    for lista in [pendientes, completadas]:
        for tarea in lista:
            if tarea["tareas"] == tarea_nombre:
                lista.remove(tarea)
                print(f"Tarea '{tarea_nombre}' eliminada correctamente.")
                return
    print(f"\nTarea '{tarea_nombre}' no encontrada.\n")

def main():
    opciones = {
        1: agregar_tarea,2: eliminar_tarea,
        3: listar_tareas,4: listar_tareas_por_estado,
        5: marcar_tarea, 6: exit}

    while True:
        print("\nMenu Principal\n")
        print("1. Agregar tarea", "\n2. Eliminar tarea", "\n3. Lista de tareas", "\n4. Tareas pendientes y completas", "\n5. Marcar tareas", "\n6. Salir\n")

        opcion = validar_entrada("Seleccione una opción: ", "num")
        funcion = opciones.get(opcion)
        funcion() if funcion else print("\nOpción no válida")

if __name__ == "__main__":
    main()
