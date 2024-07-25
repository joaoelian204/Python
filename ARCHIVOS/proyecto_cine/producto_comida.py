import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Importar Pillow
import sqlite3  # Importar sqlite3 para la base de datos
from configuracion import configurar_ventana, crear_paneles, configurar_barra_superior, configurar_menu_lateral
from eventos import toggle_panel
from colores import COLOR_CUERPO_PRINCIPAL

# Función para limpiar el contenedor principal
def limpiar_cuerpo_principal(cuerpo_principal):
    for widget in cuerpo_principal.winfo_children():
        widget.destroy()

# Función para obtener productos de la base de datos
def obtener_productos():
    conn = sqlite3.connect('cartelera.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, descripcion, precio, imagen FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos

# Función para obtener imágenes de publicidad de la base de datos
def obtener_imagenes_publicidad():
    conn = sqlite3.connect('cartelera.db')
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM imagenes_publicidad")  # Asumiendo que la columna se llama url
    imagenes = cursor.fetchall()
    conn.close()
    return [imagen[0] for imagen in imagenes]  # Devuelve solo la ruta de las imágenes

# Función para mostrar las opciones de comida
def mostrar_comida(cuerpo_principal):
    limpiar_cuerpo_principal(cuerpo_principal)

    # Crear un marco para el carrusel
    marco_carrusel = tk.Frame(cuerpo_principal, bg=COLOR_CUERPO_PRINCIPAL)
    marco_carrusel.pack(pady=40, padx=170)

    # Obtener las rutas de las imágenes del carrusel desde la base de datos
    imagenes_carrusel = obtener_imagenes_publicidad()

    # Cargar las imágenes y redimensionarlas
    imagenes = [ImageTk.PhotoImage(Image.open(img).resize((1500, 350), Image.LANCZOS)) for img in imagenes_carrusel]

    # Etiqueta para mostrar la imagen actual del carrusel
    etiqueta_imagen = tk.Label(marco_carrusel, image=imagenes[0], bg=COLOR_CUERPO_PRINCIPAL)
    etiqueta_imagen.pack()

    # Índice de la imagen actual
    indice_imagen_actual = 0

    # Función para cambiar la imagen del carrusel
    def cambiar_imagen():
        nonlocal indice_imagen_actual
        indice_imagen_actual = (indice_imagen_actual + 1) % len(imagenes)
        
        if etiqueta_imagen.winfo_exists():
            etiqueta_imagen.config(image=imagenes[indice_imagen_actual])
            cuerpo_principal.after(6000, cambiar_imagen)  # Cambiar cada 6 segundos

    # Iniciar el carrusel
    cuerpo_principal.after(5000, cambiar_imagen)

    # Crear y mostrar opciones de comida
    label_comida = tk.Label(cuerpo_principal, text="Opciones de Comida", font=("Helvetica Neue", 24, "bold"), bg=COLOR_CUERPO_PRINCIPAL, padx=10, pady=10)
    label_comida.pack(pady=10)

    # Crear un contenedor para centrar los cuadros
    contenedor = tk.Frame(cuerpo_principal, bg=COLOR_CUERPO_PRINCIPAL)
    contenedor.pack(expand=True, fill=tk.BOTH, padx=65, pady=20)

    # Obtener productos de la base de datos
    productos = obtener_productos()
    seleccionados = []
    total_precio = 0

    # Función para gestionar la selección de combos
    def añadir_al_carrito(item, cantidad):
        nonlocal total_precio
        seleccionados.append({"item": item, "cantidad": cantidad})
        total_precio += item[2] * cantidad  # item[2] es el precio
        print(f"Añadido al carrito: {item[0]} x {cantidad}")  # item[0] es el nombre
        print(f"Precio total: ${total_precio:.2f}")

    # Crear y mostrar cuadros de información para cada producto
    for idx, item in enumerate(productos):
        frame_item = tk.Frame(contenedor, bg="#ebdef0", padx=10, pady=10, highlightbackground="black", highlightthickness=1,relief="groove")
        frame_item.grid(row=idx//2, column=idx%2, padx=50, pady=10, sticky="nsew")

        # Cargar la imagen del item usando Pillow
        imagen = Image.open(item[3])  # item[3] es la ruta de la imagen
        imagen = imagen.resize((300, 200), Image.LANCZOS)  # Redimensionar la imagen
        imagen_tk = ImageTk.PhotoImage(imagen)
        label_imagen = tk.Label(frame_item, image=imagen_tk, bg="#f0f0f0", bd=0)
        label_imagen.image = imagen_tk  # Guardar una referencia a la imagen
        label_imagen.pack(pady=(10, 5))

        label_nombre = tk.Label(frame_item, text=item[0], font=("Helvetica Neue", 14, "bold"), bg="#ebdef0", fg="#333")
        label_nombre.pack(anchor="w")

        label_descripcion = tk.Label(frame_item, text=item[1], font=("Helvetica Neue", 12), bg="#ebdef0", fg="#666")
        label_descripcion.pack(anchor="w")

        label_precio = tk.Label(frame_item, text=f"${item[2]:.2f}", font=("Helvetica Neue", 12), bg="#ebdef0", fg="#333")
        label_precio.pack(anchor="w")

        cantidad_spinbox = tk.Spinbox(frame_item, from_=1, to=10, width=5)
        cantidad_spinbox.pack(pady=(5, 10))

        # Botón para añadir al carrito
        button_añadir = tk.Button(frame_item, text="Añadir", font=("Helvetica Neue", 12, "bold"), bg="#27ae60", fg="#fff",
                                bd=0, padx=10, pady=5, activebackground="#2ecc71", command=lambda i=item, c=cantidad_spinbox: añadir_al_carrito(i, int(c.get())))
        button_añadir.pack()

        frame_item.grid_propagate(False)

    for i in range(2):
        contenedor.columnconfigure(i, weight=1)
        contenedor.rowconfigure(i, weight=1)













