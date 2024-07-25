print("\n\n----------------------------------------")
print("-- Gestor de inventario de una tienda --")
print("----------------------------------------")
# Define las listas globales de productos y de historial de borrados.
granos = ["Cebada", "Farro", "Mijo", "Arroz integral", "Quinoa"]
bebidas = ["Cola", "Agua", "Jugo", "Leche", "Té verde"]
pastas = ["Espagueti", "Fettuccine", "Penne", "Macarrones", "Lasaña"]
historial_borrados = []

def validar_entrada(valor: str, tipo: str):# Función para validar la entrada del usuario.
    while True:
        entrada = input(f"{valor}")
        if tipo == "num" and entrada.isdigit():
            return int(entrada)
        elif tipo == "str" and not entrada.isdigit():
            return entrada.title().strip()
        else:
            mensaje = "Solo se aceptan " + ("números" if tipo == "num" else "texto")
            print(f"{mensaje}, ¡{valor}!")

def agregar_producto(lista, categoria):# Función para agregar productos a una categoría específica.
    producto = validar_entrada("Cuantos productos va a ingresar: ", "num")
    for i in range(producto):
        nuevo_producto = validar_entrada("Ingrese nuevo producto: ", "str").title().strip()
        lista.append(nuevo_producto)
    print(f"Se ha añadido correctamente los productos ingresados a la categoría {categoria}")
    
def eliminar_producto(lista, categoria, historial):# Función para eliminar productos de una categoría específica
    while True:
        for i, dato in enumerate(sorted(lista)):
            print(f"{i+1}. {dato}")
        producto = validar_entrada("\nCuantos productos va a eliminar: ", "num")
        for i in range(producto):
            producto_a_eliminar = validar_entrada(f"Ingrese el producto a eliminar de {categoria}: ", "str").title().strip()
            if producto_a_eliminar in lista:
                lista.remove(producto_a_eliminar)
                historial.append(producto_a_eliminar)
                print(f" ha sido eliminado los productos de la categoria: {categoria}")
            else:
                print(f"El producto no  se ha encontrado en {categoria}")

            if i == producto - 1:
                print("Todos los productos han sido eliminados.")
                return 

def mostrar_productos(lista, categoria):# Función para mostrar los productos de una categoría en un orden específico.
    print(f"\n{categoria.capitalize()}:\n")
    lista_ordenada = sorted(lista)
    for i, producto in enumerate(lista_ordenada):
        print(f"{i+1}. {producto}")
        
def mostrar_todos_los_productos_y_buscar():# Función para mostrar todos los productos y buscar un producto específico.
    while True:
        todos_los_productos = granos + bebidas + pastas
        print("\nTodos los productos:")
        print("Seleccione el orden de visualización:\n\n", "1.Ascendente\n","2.Descendente\n")
        
        opcion_orden = validar_entrada("Elige la opción: ", "num")
        if opcion_orden == 1:
            productos_ordenados = sorted(todos_los_productos)
            print("\nProductos en orden ascendente:\n")
        elif opcion_orden == 2:
            productos_ordenados = sorted(todos_los_productos, reverse=True)
            print("\nProductos en orden descendente:\n")
        else:
            print("Opción no válida.")
            continue
        for i, producto in enumerate(productos_ordenados):
            print(f"{i+1}. {producto}")
        producto_a_buscar = validar_entrada("\nIngrese el producto a buscar: ", "str").title().strip()
        repite = list(filter(lambda x: x.lower() == producto_a_buscar.lower(), todos_los_productos))
        if repite:
            print(f"\nEl producto '{producto_a_buscar}' se encuentra {len(repite)} veces en el inventario.\n")
        else:
            print(f"\nEl producto '{producto_a_buscar}' no se encuentra en el inventario.")

        retry = input("\n¿Desea intentar nuevamente? (s/n): ").lower()
        if retry!= 's':
            break

def mostrar_todos_los_eliminados():# Función para mostrar todos los productos eliminados.
    if historial_borrados:
        print("Productos eliminados:")
        for i, producto in enumerate(historial_borrados):
            print(f"{i+1}. {producto}")
    else:
        print("No hay productos eliminados.")

menu_principal = ["Agregar producto", "Eliminar producto", "Mostrar productos", "Ver productos eliminados", "Mostrar todos los productos y buscar", "Salir"]# Lista de opciones del menú principal

categorias = ["Granos", "Bebidas", "Pastas"]# Lista de categorías.

while True:# Bucle principal del programa.
    print("\n - Menú Principal\n")
    for i, opcion in enumerate(menu_principal):
        print(f"{i + 1}. {opcion}")
    
    opcion_principal = validar_entrada("\nIngresa la opción: ", "num")

    if opcion_principal == 6:
        print("\nGracias por utilizar nuestro gestor de inventarios. Vuelva pronto :) \n")
        break
    
    if opcion_principal in [1, 2, 3, 4]:
            print("\nSelecciona una categoría\n")
            for i, categoria in enumerate(categorias):
                print(f"{i + 1}. {categoria}")
            
            opcion_categoria = validar_entrada("\nIngresa la opción: ", "num")
            print(" ")
            if opcion_categoria == 1:
                categoria = "granos"
                lista = granos
            elif opcion_categoria == 2:
                categoria = "bebidas"
                lista = bebidas
            elif opcion_categoria == 3:
                categoria = "pastas"
                lista = pastas
            else:
                print("Categoría no encontrada. Intente de nuevo.")
                continue
            
            if opcion_principal == 1:
                agregar_producto(lista, categoria)
            elif opcion_principal == 2:
                eliminar_producto(lista, categoria, historial_borrados)
            elif opcion_principal == 3:
                mostrar_productos(lista, categoria)
            elif opcion_principal == 4:
                mostrar_todos_los_eliminados()
    elif opcion_principal == 5:
            mostrar_todos_los_productos_y_buscar()
    else:
        print("La opción no se encuentra, vuelva a intentar")
        
    continuar = input("\n¿Desea volver al menu principal? (s/n): ").lower()
    if continuar == 'n':
        print("\nGracias por utilizar nuestro gestor de inventarios. Vuelva pronto :) \n")
        break
    else:
        print("La opcion ingresada no existe en el sistema. VUELVA A INTENTAR..")
        continuar = input("\n¿Desea volver al menu principal? (s/n): ").lower()
