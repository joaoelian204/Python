granos = ["Arroz","Lenteja","Maiz","Centeno","Trigo"]
bebidas = ["Agua","Coca","Pepsi","Jugo de naranja","Agua De Coco"]
pasta = ["Fideos Instantaneos","Canelones","Pasta De Lasagna","Fideos Sabor Pollo","Fideo De Tornillo"]
productos_eliminados = []

def menu_principal():
    print("\n1. Eliminar producto\n2. Agregar producto\n3. Mostrar listra de productos eliminados\n4. Reporte\n5. Salir\n")
    return
def menu_lista():
    print("\n1. Granos\n2. bebidas\n3. pasta\n4. salir\n")        
    return

# validacion de todos los productos 
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

#Mostrar listass
def mostrar_lista(producto):
    for i in producto:
        print(f"* {i}")
    print("\n")

#Selecciona la lista para eliminar
def eliminar_producto():
    menu_lista()
    numero = validar_entrada("Seleccione la opcion:  ", "num")
    if numero == 1:
        iniciar_eliminar_producto(granos)
    elif numero == 2:
        iniciar_eliminar_producto(bebidas)
    elif numero == 3:
        iniciar_eliminar_producto(pasta)
    elif numero == 4:
        iniciar()
    else:
        print("ingrese un valor valido")
    
#Elimina el producto que se ingrese
def iniciar_eliminar_producto(lista):
    mostrar_lista(lista)
    cantidad = validar_entrada("Cuantos productos va a eliminar: ","num")    
    for i in range(0,cantidad):
        producto_a_eliminar = validar_entrada("Ingrese el producto que desea eliminar: ","str")
        if producto_a_eliminar in lista:
            lista.remove(producto_a_eliminar)
            productos_eliminados.append(producto_a_eliminar)
            print(f"Producto '{producto_a_eliminar}' eliminado correctamente.")
        else:
            print(f"El producto '{producto_a_eliminar}' no está en la lista.")
    mostrar_lista(lista)

#Se agrega un producto a una lista
def agregar_producto():
    menu_lista()
    numero = validar_entrada("Seleccione la opcion:  ", "num")
    if numero == 1:
        aumentar_producto(granos)
    elif numero == 2:
        aumentar_producto(bebidas)
    elif numero == 3:
        aumentar_producto(pasta)
    elif numero == 4:
        iniciar()
    else:
        print("ingrese un valor valido")

def aumentar_producto(lista):           
    nuevo_producto = validar_entrada("Ingrese el nombre del nuevo producto: ","str")
    lista.append(nuevo_producto)
    mostrar_lista(lista)
    print("\n")
    
def reporte(granos,bebidas,pasta):
    lista_total = []
    lista_total.extend(granos)
    lista_total.extend(bebidas)
    lista_total.extend(pasta)
    opcion = validar_entrada("Mostar report\n1. ascendente\n2. decendente\n","num")
    while True:
        if opcion == 1:
            # Muestra todas las listas juntas de manera ascendente
            print("Todas las listas juntas de manera ascendente:")
            mostrar_lista(sorted(lista_total)) 
            buscar_producto(lista_total)
            break 
        elif opcion == 2:
            # Muestra todas las listas juntas de manera descendente
            print("nTodas las listas juntas de manera descendente:")
            mostrar_lista(sorted(lista_total, reverse=True))
            buscar_producto(lista_total)
            break
        else:
            print("Ingrese una opcion correcta")

def buscar_producto(lista):
    nombre = validar_entrada("Cual producto desea buscar: ","str")
    texto = print(f"El producto '{nombre}' se repite {lista.count(nombre)} veces en la lista.")
    return texto

def iniciar():
    while True:
        menu_principal()
        numero = validar_entrada("Seleccione la opcion  ", "num")
        if numero == 1:
            eliminar_producto()
        elif numero == 2:
            agregar_producto()
        elif numero == 3:
            print("Los productos eliminados son:")
            mostrar_lista(productos_eliminados)
        elif numero == 4:
            reporte(granos,bebidas,pasta)
        elif numero == 5:
            break
        else:
            print("ingrese un valor valido")

iniciar()