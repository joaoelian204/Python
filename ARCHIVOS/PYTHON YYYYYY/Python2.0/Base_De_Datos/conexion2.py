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
    productos = cursorBD.fetchall()
    for producto in productos:
        print(producto)

def insertar_producto_db(nombre, categoria):
    cursorBD.execute('''INSERT INTO PRODUCTO (NOMBRE, CATEGORIA) VALUES (?, ?)''', (nombre, categoria))
    conexion.commit()

def seleccionar_productos_db():
    cursorBD.execute('''SELECT * FROM PRODUCTO''')
    lista = cursorBD.fetchall()
    return lista

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

# Funciones del menú
def validar_entrada(valor: str, tipo: str):
    while True:
        entrada = input(f"{valor}")
        if tipo == "num" and entrada.isdigit():
            return int(entrada)
        elif tipo == "str" and not entrada.isdigit():
            return entrada.title().strip()
        else:
            mensaje = "Solo se aceptan " + ("números" if tipo == "num" else "texto")
            print(f"{mensaje}, ¡{valor}!")

def agregar_producto(categoria):
    cantidad = validar_entrada("\nCuantos productos va a ingresar: ", "num")
    for _ in range(cantidad):
        nombre_producto = validar_entrada("Ingrese nuevo producto: ", "str")
        insertar_producto_db(nombre_producto, categoria)
    print(f"\nSe ha añadido correctamente los productos ingresados a la categoría {categoria}")

def eliminar_producto(categoria):
    while True:
        cursorBD.execute("SELECT * FROM PRODUCTO WHERE CATEGORIA = ?", (categoria,))
        productos = cursorBD.fetchall()
        for producto in productos:
            print(producto)
        producto_a_eliminar = validar_entrada("\nIngrese el nombre del producto a eliminar: ", "str")
        cursorBD.execute("SELECT * FROM PRODUCTO WHERE NOMBRE = ? AND CATEGORIA = ?", (producto_a_eliminar, categoria))
        producto = cursorBD.fetchone()
        if producto:
            eliminar_producto_db(producto[0])
            print(f"El producto '{producto_a_eliminar}' ha sido eliminado de la categoría {categoria}")
        else:
            print(f"El producto '{producto_a_eliminar}' no se encontró en la categoría {categoria}")

        continuar = input("\n¿Desea eliminar otro producto? (s/n): ").lower()
        if continuar != 's':
            break

def mostrar_productos(categoria):
    cursorBD.execute("SELECT * FROM PRODUCTO WHERE CATEGORIA = ?", (categoria,))
    productos = cursorBD.fetchall()
    print(f"\n{categoria.capitalize()}:\n")
    for i, producto in enumerate(productos, start=1):
        print(f"{i}. {producto[1]}")

def mostrar_todos_los_productos_y_buscar():
    while True:
        cursorBD.execute("SELECT * FROM PRODUCTO")
        todos_los_productos = cursorBD.fetchall()
        opcion_orden = validar_entrada("Seleccione el orden de visualización (1.Ascendente, 2.Descendente): ", "num")
        if opcion_orden == 1:
            productos_ordenados = sorted(todos_los_productos, key=lambda x: x[1])
            print("\nProductos en orden ascendente:\n")
        elif opcion_orden == 2:
            productos_ordenados = sorted(todos_los_productos, key=lambda x: x[1], reverse=True)
            print("\nProductos en orden descendente:\n")
        else:
            print("\nOpción no válida.")
            continue
        for i, producto in enumerate(productos_ordenados, start=1):
            print(f"{i}. {producto[1]}")

        producto_a_buscar = validar_entrada("\nIngrese el producto a buscar: ", "str")
        encontrados = [p for p in todos_los_productos if p[1].lower() == producto_a_buscar.lower()]
        if encontrados:
            print(f"\nEl producto '{producto_a_buscar}' se encuentra {len(encontrados)} veces en el inventario.\n")
        else:
            print(f"\nEl producto '{producto_a_buscar}' no se encuentra en el inventario.")

        retry = input("\n¿Desea intentar nuevamente? (s/n): ").lower()
        if retry != 's':
            break

def mostrar_todos_los_eliminados():
    cursorBD.execute("SELECT * FROM HISTORIAL_BORRADOS")
    productos_eliminados = cursorBD.fetchall()
    if productos_eliminados:
        print("Productos eliminados:")
        for producto in productos_eliminados:
            print(f"ID: {producto[0]}, Nombre: {producto[1]}, Categoría: {producto[2]}, Fecha de eliminación: {producto[3]}")
    else:
        print("No hay productos eliminados.")

# Menú principal
menu_principal = ["Agregar producto", "Eliminar producto", "Mostrar productos", "Ver productos eliminados", "Mostrar todos los productos y buscar", "Salir"]
categorias = ["Granos", "Bebidas", "Pastas"]

while True:
    print("\n - Menú Principal\n")
    for i, opcion in enumerate(menu_principal, start=1):
        print(f"{i}. {opcion}")

    opcion_principal = validar_entrada("\nIngresa la opción: ", "num")

    if opcion_principal == 6:
        print("\nGracias por utilizar nuestro gestor de inventarios. Vuelva pronto :) \n")
        break

    if opcion_principal in [1, 2, 3, 4]:
        print("\nSelecciona una categoría\n")
        for i, categoria in enumerate(categorias, start=1):
            print(f"{i}. {categoria}")

        opcion_categoria = validar_entrada("\nIngresa la opción: ", "num")

        print()       
        if opcion_categoria == 1:
            categoria = "Granos"
        elif opcion_categoria == 2:
            categoria = "Bebidas"
        elif opcion_categoria == 3:
            categoria = "Pastas"
        else:
            print("Categoría no encontrada. Intente de nuevo.")
            continue

        if opcion_principal == 1:
            agregar_producto(categoria)
        elif opcion_principal == 2:
            eliminar_producto(categoria)
        elif opcion_principal == 3:
            mostrar_productos(categoria)
        elif opcion_principal == 4:
            mostrar_todos_los_eliminados()
    elif opcion_principal == 5:
        mostrar_todos_los_productos_y_buscar()
    else:
        print("La opción no se encuentra, vuelva a intentar")

    continuar = input("\n¿Desea volver al menu principal? (s/n): ").lower()
    if continuar != 's':
        print("\nGracias por utilizar nuestro gestor de inventarios. Vuelva pronto :) \n")
        break

# Cerrar la conexión al final del programa
conexion.close()
