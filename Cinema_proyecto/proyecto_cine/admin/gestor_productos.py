import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from PIL import Image, ImageTk
import sqlite3

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

# Función para agregar un nuevo producto
def agregar_producto(nombre, descripcion, precio, imagen, cuerpo_principal):
    conn = sqlite3.connect('cartelera.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, descripcion, precio, imagen) VALUES (?, ?, ?, ?)", 
                   (nombre, descripcion, precio, imagen))
    conn.commit()
    conn.close()
    messagebox.showinfo("Éxito", "Producto agregado exitosamente.")
    mostrar_productos(cuerpo_principal)  # Actualiza la vista

# Función para eliminar un producto
def eliminar_producto(nombre, cuerpo_principal):
    conn = sqlite3.connect('cartelera.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE nombre=?", (nombre,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Éxito", "Producto eliminado exitosamente.")
    mostrar_productos(cuerpo_principal)  # Actualiza la vista

# Función para mostrar un diálogo de eliminación
def dialogo_eliminar_producto(nombre, cuerpo_principal):
    if messagebox.askyesno("Eliminar Producto", f"¿Está seguro de que desea eliminar el producto '{nombre}'?"):
        eliminar_producto(nombre, cuerpo_principal)

# Función para seleccionar una imagen desde el sistema
def seleccionar_imagen(entrada_imagen, label_imagen_preview):
    archivo = filedialog.askopenfilename(
        title="Seleccionar imagen", 
        filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.gif"), ("Todos los archivos", "*.*")]
    )
    if archivo:
        entrada_imagen.delete(0, tk.END)  # Limpiar entrada de texto
        entrada_imagen.insert(0, archivo)  # Mostrar la ruta en la entrada
        # Mostrar la imagen seleccionada
        imagen = Image.open(archivo)
        imagen.thumbnail((200, 200))  # Ajustar tamaño
        imagen_tk = ImageTk.PhotoImage(imagen)
        label_imagen_preview.config(image=imagen_tk)
        label_imagen_preview.image = imagen_tk  # Mantener referencia

# Función para editar un producto
def editar_producto(nombre, cuerpo_principal):
    # Obtener datos del producto
    conn = sqlite3.connect('cartelera.db')
    cursor = conn.cursor()
    cursor.execute("SELECT descripcion, precio, imagen FROM productos WHERE nombre=?", (nombre,))
    producto = cursor.fetchone()
    conn.close()

    # Crear ventana de edición
    ventana_edicion = tk.Toplevel()
    ventana_edicion.title("Editar Producto")
    ventana_edicion.configure(bg="white")

    tk.Label(ventana_edicion, text="Editar Producto", font=("Helvetica Neue", 18, "bold"), bg="white").pack(pady=10)

    tk.Label(ventana_edicion, text="Descripción:", bg="white").pack(pady=5)
    entrada_descripcion = tk.Entry(ventana_edicion, width=50)
    entrada_descripcion.insert(0, producto[0])
    entrada_descripcion.pack(pady=5)

    tk.Label(ventana_edicion, text="Precio:", bg="white").pack(pady=5)
    entrada_precio = tk.Entry(ventana_edicion, width=50)
    entrada_precio.insert(0, producto[1])
    entrada_precio.pack(pady=5)

    tk.Label(ventana_edicion, text="Imagen:", bg="white").pack(pady=5)
    entrada_imagen = tk.Entry(ventana_edicion, width=50)
    entrada_imagen.insert(0, producto[2])
    entrada_imagen.pack(pady=5)

    label_imagen_preview = tk.Label(ventana_edicion, bg="white")
    label_imagen_preview.pack(pady=5)

    button_seleccionar = tk.Button(ventana_edicion, text="Seleccionar Imagen", command=lambda: seleccionar_imagen(entrada_imagen, label_imagen_preview))
    button_seleccionar.pack(pady=5)

    # Función para guardar cambios
    def guardar_cambios():
        descripcion = entrada_descripcion.get()
        precio = entrada_precio.get()
        imagen = entrada_imagen.get().strip()  # Asegúrate de que no haya espacios

        if descripcion and precio and imagen:
            try:
                editar_producto_bd(nombre, descripcion, float(precio), imagen, cuerpo_principal)
                ventana_edicion.destroy()
            except ValueError:
                messagebox.showerror("Error", "El precio debe ser un número válido.")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos deben ser completados.")

    # Frame para botones
    frame_botones = tk.Frame(ventana_edicion, bg="black", padx=10, pady=10)
    frame_botones.pack(pady=20, fill=tk.X)

    button_guardar = tk.Button(frame_botones, text="Guardar cambios", command=guardar_cambios, bg="white", fg="black")
    button_guardar.pack(side=tk.LEFT, padx=5)

    button_cancelar = tk.Button(frame_botones, text="Cancelar", command=ventana_edicion.destroy, bg="white", fg="black")
    button_cancelar.pack(side=tk.RIGHT, padx=5)

# Función para editar en la base de datos
def editar_producto_bd(nombre, descripcion, precio, imagen, cuerpo_principal):
    conn = sqlite3.connect('cartelera.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE productos SET descripcion=?, precio=?, imagen=? WHERE nombre=?", 
                   (descripcion, precio, imagen, nombre))
    conn.commit()
    conn.close()
    messagebox.showinfo("Éxito", "Producto editado exitosamente.")
    mostrar_productos(cuerpo_principal)  # Actualiza la vista

# Función para mostrar los productos en el contenedor
# Función para mostrar los productos en el contenedor
def mostrar_productos(cuerpo_principal):
    limpiar_cuerpo_principal(cuerpo_principal)

    productos = obtener_productos()

    contenedor_productos = tk.Frame(cuerpo_principal, bg="white")
    contenedor_productos.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    # Variable para contar la posición en la cuadrícula
    posicion = 0
    fila_actual = None  # Variable para almacenar la referencia a la fila actual

    for idx, item in enumerate(productos):
        if idx % 5 == 0:
            # Crear una nueva fila en la cuadrícula
            fila_actual = tk.Frame(contenedor_productos, bg="white")
            fila_actual.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        frame_item = tk.Frame(fila_actual, bg="#3498db", padx=20, pady=20, width=200, height=250, highlightbackground="#000", highlightthickness=2)
        frame_item.pack(side=tk.LEFT, padx=10, pady=10)

        imagen = Image.open(item[3])
        imagen = imagen.resize((300, 250), Image.LANCZOS)
        imagen_tk = ImageTk.PhotoImage(imagen)
        label_imagen = tk.Label(frame_item, image=imagen_tk, bg="#3498db")
        label_imagen.image = imagen_tk
        label_imagen.pack(pady=5)

        label_nombre = tk.Label(frame_item, text=item[0], font=("Helvetica Neue", 12, "bold"), bg="#3498db", fg="#fff")
        label_nombre.pack(anchor="w")

        label_descripcion = tk.Label(frame_item, text=item[1], font=("Helvetica Neue", 10), bg="#3498db", fg="#ecf0f1")
        label_descripcion.pack(anchor="w")

        label_precio = tk.Label(frame_item, text=f"${item[2]:.2f}", font=("Helvetica Neue", 10), bg="#3498db", fg="#ecf0f1")
        label_precio.pack(anchor="w")

        button_eliminar = tk.Button(frame_item, text="Eliminar", command=lambda nombre=item[0]: dialogo_eliminar_producto(nombre, cuerpo_principal), bg="#e74c3c", fg="white")
        button_eliminar.pack(side=tk.LEFT, padx=5, pady=5)

        button_editar = tk.Button(frame_item, text="Editar", command=lambda nombre=item[0]: editar_producto(nombre, cuerpo_principal), bg="#2ecc71", fg="white")
        button_editar.pack(side=tk.RIGHT, padx=5, pady=5)

    button_agregar = tk.Button(cuerpo_principal, text="Agregar Producto", command=lambda: ventana_agregar_producto(cuerpo_principal), bg="#3498db", fg="white", font=("Helvetica Neue", 12, "bold"))
    button_agregar.pack(side=tk.BOTTOM, pady=10)

# Función para abrir la ventana de agregar producto
def ventana_agregar_producto(cuerpo_principal):
    ventana_agregar = tk.Toplevel()
    ventana_agregar.title("Agregar Producto")
    ventana_agregar.configure(bg="white")

    tk.Label(ventana_agregar, text="Agregar Producto", font=("Helvetica Neue", 18, "bold"), bg="white").pack(pady=10)

    tk.Label(ventana_agregar, text="Nombre:", bg="white").pack(pady=5)
    entrada_nombre = tk.Entry(ventana_agregar, width=50)
    entrada_nombre.pack(pady=5)

    tk.Label(ventana_agregar, text="Descripción:", bg="white").pack(pady=5)
    entrada_descripcion = tk.Entry(ventana_agregar, width=50)
    entrada_descripcion.pack(pady=5)

    tk.Label(ventana_agregar, text="Precio:", bg="white").pack(pady=5)
    entrada_precio = tk.Entry(ventana_agregar, width=50)
    entrada_precio.pack(pady=5)

    tk.Label(ventana_agregar, text="Imagen:", bg="white").pack(pady=5)
    entrada_imagen = tk.Entry(ventana_agregar, width=50)
    entrada_imagen.pack(pady=5)

    label_imagen_preview = tk.Label(ventana_agregar, bg="white")
    label_imagen_preview.pack(pady=5)

    button_seleccionar = tk.Button(ventana_agregar, text="Seleccionar Imagen", command=lambda: seleccionar_imagen(entrada_imagen, label_imagen_preview))
    button_seleccionar.pack(pady=5)

    def agregar():
        nombre = entrada_nombre.get()
        descripcion = entrada_descripcion.get()
        precio = entrada_precio.get()
        imagen = entrada_imagen.get().strip()

        if nombre and descripcion and precio and imagen:
            try:
                agregar_producto(nombre, descripcion, float(precio), imagen, cuerpo_principal)
                ventana_agregar.destroy()
            except ValueError:
                messagebox.showerror("Error", "El precio debe ser un número válido.")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos deben ser completados.")

    # Frame para botones
    frame_botones = tk.Frame(ventana_agregar, bg="black", padx=10, pady=10)
    frame_botones.pack(pady=20, fill=tk.X)

    button_guardar = tk.Button(frame_botones, text="Agregar", command=agregar, bg="white", fg="black")
    button_guardar.pack(side=tk.LEFT, padx=5)

    button_cancelar = tk.Button(frame_botones, text="Cancelar", command=ventana_agregar.destroy, bg="white", fg="black")
    button_cancelar.pack(side=tk.RIGHT, padx=5)








