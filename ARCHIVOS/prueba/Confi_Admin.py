import tkinter as tk
from tkinter import font, messagebox, filedialog
from PIL import Image, ImageTk
import sqlite3
from colores import *
import os

# Constantes de colores y configuraciones visuales
ANCHO_IMAGEN = 330
ALTO_IMAGEN = 300

# Ruta a la base de datos SQLite
DB_FILE = 'cartelera.db'

# Diccionario para almacenar referencias a las imágenes cargadas
imagenes_pelis = {}

# Función para conectar a la base de datos
def conectar_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    return conn, cursor

# Función para cerrar la conexión a la base de datos
def cerrar_db(conn):
    if conn:
        conn.close()

# Función para crear la tabla de películas si no existe
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

# Función para insertar una película en la base de datos
def insertar_pelicula(titulo, genero, duracion, sinopsis, imagen):
    conn, cursor = conectar_db()
    cursor.execute('''
        INSERT INTO peliculas (titulo, genero, duracion, sinopsis, imagen)
        VALUES (?, ?, ?, ?, ?)
    ''', (titulo, genero, duracion, sinopsis, imagen))
    conn.commit()
    cerrar_db(conn)

# Función para actualizar los datos de una película
def actualizar_pelicula(id_pelicula, titulo, genero, duracion, sinopsis, imagen):
    conn, cursor = conectar_db()
    cursor.execute('''
        UPDATE peliculas
        SET titulo=?, genero=?, duracion=?, sinopsis=?, imagen=?
        WHERE id=?
    ''', (titulo, genero, duracion, sinopsis, imagen, id_pelicula))
    conn.commit()
    cerrar_db(conn)

# Función para eliminar una película de la base de datos
def eliminar_pelicula(id_pelicula):
    conn, cursor = conectar_db()
    cursor.execute('DELETE FROM peliculas WHERE id=?', (id_pelicula,))
    conn.commit()
    cerrar_db(conn)

# Función para cargar la cartelera desde la base de datos
def cargar_cartelera():
    conn, cursor = conectar_db()
    cursor.execute('SELECT id, titulo, genero, duracion, sinopsis, imagen FROM peliculas')
    peliculas = cursor.fetchall()
    cerrar_db(conn)
    return peliculas

# Función para seleccionar una película y mostrar sus detalles
def seleccionar_pelicula(id_pelicula):
    conn, cursor = conectar_db()
    cursor.execute('SELECT id, titulo, genero, duracion, sinopsis, imagen FROM peliculas WHERE id=?', (id_pelicula,))
    pelicula = cursor.fetchone()
    cerrar_db(conn)
    return pelicula

# Función para mostrar un cuadro de diálogo para seleccionar una imagen
def seleccionar_imagen():
    filename = filedialog.askopenfilename(title="Seleccionar Imagen", filetypes=[("Archivos de Imagen", "*.png *.jpg *.jpeg")])
    return filename

# Función para mostrar un mensaje de confirmación para eliminar una película
def confirmar_eliminar(id_pelicula, ventana):
    if messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro de eliminar esta película?"):
        eliminar_pelicula(id_pelicula)
        messagebox.showinfo("Eliminación Exitosa", "La película ha sido eliminada.")
        ventana.destroy()
        cargar_cartelera()  # Asegúrate de pasar el argumento cuerpo_principal aquí

# Función para crear botones con estilo
def crear_boton(parent, texto, comando, color_fondo, fila, columna, padx=10, pady=10):
    boton = tk.Button(parent, text=texto, command=comando, bg=color_fondo, fg='#fff')
    boton.grid(row=fila, column=columna, padx=padx, pady=pady)
    return boton

# Función para configurar los eventos de hover en botones
def bind_hover_events(button):
    button.bind("<Enter>", lambda e: button.config(bg="#4CAF50"))  # Color de fondo cuando el mouse entra
    button.bind("<Leave>", lambda e: button.config(bg="#2196F3"))  # Color de fondo normal

# Función para crear etiquetas y entradas con estilo
def crear_label_y_entry(parent, texto_label, valor_entry, row, column):
    estilo_label = {'bg': '#f0f0f0', 'fg': '#333', 'font': ('Arial', 11)}
    estilo_entry = {'bg': '#fff', 'fg': '#333', 'font': ('Arial', 11)}

    label = tk.Label(parent, text=texto_label, **estilo_label)
    label.grid(row=row, column=column, padx=10, pady=10, sticky=tk.E)

    entry = tk.Entry(parent, width=40, **estilo_entry)
    entry.grid(row=row, column=column+1, padx=10, pady=10)
    entry.insert(0, valor_entry)

    return entry  # Retorna la entrada para que puedas acceder a ella si es necesario

# Función para mostrar la ventana de edición de una película
def mostrar_ventana_edicion(id_pelicula, cuerpo_principal):
    ventana_edicion = tk.Toplevel()
    ventana_edicion.title("Editar Película")
    ventana_edicion.configure(bg='#f0f0f0')  # Color de fondo para la ventana

    pelicula = seleccionar_pelicula(id_pelicula)

    # Crear etiquetas y entradas usando la función reutilizable
    entry_titulo = crear_label_y_entry(ventana_edicion, "Título:", pelicula[1], 0, 0)
    entry_genero = crear_label_y_entry(ventana_edicion, "Género:", pelicula[2], 1, 0)
    entry_duracion = crear_label_y_entry(ventana_edicion, "Duración (minutos):", pelicula[3], 2, 0)
    
    estilo_label_sinopsis = {'bg': '#f0f0f0', 'fg': '#333', 'font': ('Arial', 11)}
    estilo_entry_sinopsis = {'bg': '#fff', 'fg': '#333', 'font': ('Arial', 11)}

    label_sinopsis = tk.Label(ventana_edicion, text="Sinopsis:", **estilo_label_sinopsis)
    label_sinopsis.grid(row=3, column=0, padx=10, pady=10, sticky=tk.NE)

    entry_sinopsis = tk.Text(ventana_edicion, width=40, height=10, **estilo_entry_sinopsis)
    entry_sinopsis.grid(row=3, column=1, padx=10, pady=10, sticky=tk.NSEW)
    entry_sinopsis.insert(tk.END, pelicula[4])

    entry_imagen = crear_label_y_entry(ventana_edicion, "Imagen:", pelicula[5], 4, 0)
    
    def seleccionar_imagen_y_mostrar():
        filename = seleccionar_imagen()
        if filename:
            entry_imagen.config(state="normal")
            entry_imagen.delete(0, tk.END)
            entry_imagen.insert(0, filename)
            entry_imagen.config(state="readonly")

    boton_seleccionar_imagen = tk.Button(ventana_edicion, text="Seleccionar Imagen", command=seleccionar_imagen_y_mostrar, bg='#4CAF50', fg='#fff')
    boton_seleccionar_imagen.grid(row=4, column=2, padx=10, pady=10)

    def guardar_cambios():
        titulo = entry_titulo.get()
        genero = entry_genero.get()
        duracion = entry_duracion.get()
        sinopsis = entry_sinopsis.get("1.0", tk.END).strip()  # Aquí se corrige el error
        imagen = entry_imagen.get()

        if titulo and duracion:
            actualizar_pelicula(id_pelicula, titulo, genero, duracion, sinopsis, imagen)
            messagebox.showinfo("Actualización Exitosa", "Los cambios han sido guardados.")
            ventana_edicion.destroy()
            mostrar_cartelera(cuerpo_principal)  # Actualizar la cartelera después de guardar cambios
        else:
            messagebox.showerror("Error", "Por favor, completa todos los campos obligatorios.")

    boton_guardar = tk.Button(ventana_edicion, text="Guardar Cambios", command=guardar_cambios, bg='#2196F3', fg='#fff')
    boton_guardar.grid(row=5, column=1, padx=10, pady=10)

    boton_cancelar = tk.Button(ventana_edicion, text="Cancelar", command=ventana_edicion.destroy, bg='#FF5722', fg='#fff')
    boton_cancelar.grid(row=5, column=2, padx=10, pady=10)

    boton_eliminar = tk.Button(ventana_edicion, text="Eliminar Película", command=lambda: confirmar_eliminar(id_pelicula, ventana_edicion), bg='#f44336', fg='#fff')
    boton_eliminar.grid(row=6, column=1, columnspan=2, padx=10, pady=10)

    # Ajustar el tamaño de la ventana para que se adapte al contenido
    ventana_edicion.resizable(False, False)

def mostrar_ventana_agregar(cuerpo_principal):
    ventana_agregar = tk.Toplevel()
    ventana_agregar.title("Agregar Película")
    ventana_agregar.configure(bg='#f0f0f0')  # Color de fondo para la ventana

    # Corregir llamada a crear_label_y_entry para incluir los cinco argumentos requeridos
    entry_titulo = crear_label_y_entry(ventana_agregar, "Título:", "", 0, 0)
    entry_genero = crear_label_y_entry(ventana_agregar, "Género:", "", 1, 0)
    entry_duracion = crear_label_y_entry(ventana_agregar, "Duración (minutos):", "", 2, 0)

    # Estilo para la sinopsis y entrada de imagen
    estilo_entry = {'bg': '#fff', 'fg': '#333', 'font': ('Arial', 11)}
    estilo_label = {'bg': '#f0f0f0', 'fg': '#333', 'font': ('Arial', 11)}

    label_sinopsis = tk.Label(ventana_agregar, text="Sinopsis:", **estilo_label)
    label_sinopsis.grid(row=3, column=0, padx=10, pady=10, sticky=tk.NE)
    entry_sinopsis = tk.Text(ventana_agregar, width=40, height=10, **estilo_entry)
    entry_sinopsis.grid(row=3, column=1, padx=10, pady=10, sticky=tk.NSEW)

    label_imagen = tk.Label(ventana_agregar, text="Imagen:", **estilo_label)
    label_imagen.grid(row=4, column=0, padx=10, pady=10, sticky=tk.E)
    entry_imagen = tk.Entry(ventana_agregar, width=40, state="readonly", **estilo_entry)
    entry_imagen.grid(row=4, column=1, padx=10, pady=10)

    def seleccionar_imagen_y_mostrar():
        filename = seleccionar_imagen()
        if filename:
            entry_imagen.config(state="normal")
            entry_imagen.delete(0, tk.END)
            entry_imagen.insert(0, filename)
            entry_imagen.config(state="readonly")

    crear_boton(ventana_agregar, "Seleccionar Imagen", seleccionar_imagen_y_mostrar, '#4CAF50', 4, 2)

    def guardar_nueva_pelicula():
        titulo = entry_titulo.get()
        genero = entry_genero.get()
        duracion = entry_duracion.get()
        sinopsis = entry_sinopsis.get("1.0", tk.END).strip()
        imagen = entry_imagen.get()

        if titulo and duracion:
            insertar_pelicula(titulo, genero, duracion, sinopsis, imagen)
            messagebox.showinfo("Película Agregada", "La película ha sido agregada correctamente.")
            ventana_agregar.destroy()
            mostrar_cartelera(cuerpo_principal)  # Actualizar la cartelera después de agregar la película
        else:
            messagebox.showerror("Error", "Por favor, completa todos los campos obligatorios.")

    crear_boton(ventana_agregar, "Guardar Película", guardar_nueva_pelicula, '#2196F3', 5, 1)
    crear_boton(ventana_agregar, "Cancelar", ventana_agregar.destroy, '#FF5722', 5, 2)

    # Ajustar el tamaño de la ventana para que se adapte al contenido
    ventana_agregar.resizable(False, False)


# Función para mostrar la cartelera en la interfaz gráfica
def mostrar_cartelera(cuerpo_principal):
    peliculas = cargar_cartelera()

    # Limpiar cualquier widget previamente mostrado en cuerpo_principal
    for widget in cuerpo_principal.winfo_children():
        widget.destroy()

    # Definir el número de columnas para la disposición de películas
    columnas = 5

    # Iterar sobre cada película y mostrar sus detalles
    for idx, pelicula in enumerate(peliculas):
        titulo = pelicula[1]
        genero = pelicula[2]
        duracion = pelicula[3]
        sinopsis = pelicula[4]

        # Intentar cargar la imagen de la película
        try:
            # Verificar si la imagen está en el diccionario de imágenes cargadas
            if pelicula[5] in imagenes_pelis:
                foto = imagenes_pelis[pelicula[5]]
            else:
                # Cargar la imagen desde el archivo si no está en el diccionario
                imagen = Image.open(pelicula[5])
                imagen = imagen.resize((ANCHO_IMAGEN, ALTO_IMAGEN), Image.LANCZOS)
                foto = ImageTk.PhotoImage(imagen)
                imagenes_pelis[pelicula[5]] = foto
        except Exception as e:
            # Manejar errores al cargar la imagen
            print(f"Error al cargar la imagen {pelicula[5]}: {e}")
            foto = None

        # Crear un frame para mostrar la información de la película
        frame_pelicula = tk.Frame(cuerpo_principal, bd=2, relief=tk.RAISED, padx=10, pady=10, bg="#000000")
        frame_pelicula.grid(row=idx // columnas, column=idx % columnas, padx=10, pady=10)

        # Mostrar la imagen de la película si está disponible
        if foto:
            label_imagen = tk.Label(frame_pelicula, image=foto)
            label_imagen.image = foto
            label_imagen.pack()

        # Mostrar título, género y duración de la película
        label_titulo = tk.Label(frame_pelicula, text=titulo, font=("Arial", 14), bg="#000000", fg="#ffffff")
        label_titulo.pack()

        label_genero = tk.Label(frame_pelicula, text=f"Género: {genero}", bg="#000000", fg="#ffffff")
        label_genero.pack()

        label_duracion = tk.Label(frame_pelicula, text=f"Duración: {duracion} min", bg="#000000", fg="#ffffff")
        label_duracion.pack()

        # Botón para editar la película
        boton_editar = tk.Button(frame_pelicula, text="Editar", command=lambda id_pelicula=pelicula[0]: mostrar_ventana_edicion(id_pelicula, cuerpo_principal))
        boton_editar.pack()
        

# Función para alternar el menú lateral
def toggle_panel(menu_lateral):
    if menu_lateral.winfo_viewable():
        menu_lateral.pack_forget()
    else:
        menu_lateral.pack(side=tk.LEFT, fill=tk.Y)


# Configuración de la ventana principal
def configurar_ventana(root):
    root.title("Plataforma de Cine")
    root.geometry("1920x1010")
    root.resizable(False, False)

# Creación de paneles de la interfaz
def crear_paneles(root):
    barra_superior = tk.Frame(root, bg=COLOR_BARRA_SUPERIOR, height=50)
    barra_superior.pack(side=tk.TOP, fill=tk.BOTH)

    menu_lateral = tk.Frame(root, bg=COLOR_MENU_LATERAL, width=200)
    menu_lateral.pack(side=tk.LEFT, fill=tk.Y)

    canvas = tk.Canvas(root, bg=COLOR_CUERPO_PRINCIPAL)
    canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    cuerpo_principal = tk.Frame(canvas, bg=COLOR_CUERPO_PRINCIPAL)
    canvas.create_window((0, 0), window=cuerpo_principal, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    cuerpo_principal.bind("<Configure>", on_configure)

    return barra_superior, menu_lateral, cuerpo_principal

# Configuración de la barra superior
def configurar_barra_superior(barra_superior, toggle_panel_callback):
    font_awesome = font.Font(family='FontAwesome', size=15)

    label_titulo = tk.Label(barra_superior, text="Plataforma Cine", fg="#fff", font=("Roboto", 15), bg=COLOR_BARRA_SUPERIOR, pady=10, highlightthickness=0)
    label_titulo.pack(side=tk.LEFT, padx=10)

    button_menu_lateral = tk.Button(barra_superior, text="☰", font=font_awesome, command=toggle_panel_callback, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="#fff", padx=10)
    button_menu_lateral.pack(side=tk.LEFT, padx=10)

    label_info = tk.Label(barra_superior, text="joaoM@example.com", fg="#fff", font=("Roboto", 10), bg=COLOR_BARRA_SUPERIOR, padx=10)
    label_info.pack(side=tk.RIGHT)

# Configuración del menú lateral
def configurar_menu_lateral(menu_lateral, cuerpo_principal, root):
    font_awesome = font.Font(family='FontAwesome', size=15)

    buttons_info = [
        ("Editar Película", "🎬", lambda: mostrar_cartelera(cuerpo_principal)),
        ("Añadir Película", "➕", lambda: mostrar_ventana_agregar(cuerpo_principal)),
        #("Cerrar Sesión", "🚪", lambda: mostrar_login(root))
    ]

    for txt, icon, command in buttons_info:
        button = tk.Button(menu_lateral, text=f"{icon} {txt}", anchor="w", font=font_awesome, bd=0, bg=COLOR_BOTON_NORMAL, fg="#fff", width=15, height=1, command=command)
        button.pack(side=tk.TOP, pady=10, padx=20, fill=tk.X)
        bind_hover_events(button)

# Función principal de la aplicación
def main():
    root = tk.Tk()
    configurar_ventana(root)

    barra_superior, menu_lateral, cuerpo_principal = crear_paneles(root)
    configurar_barra_superior(barra_superior, lambda: toggle_panel(menu_lateral))
    configurar_menu_lateral(menu_lateral, cuerpo_principal, root)

    mostrar_cartelera(cuerpo_principal)

    root.mainloop()

# Crear la base de datos y la tabla si no existe
crear_tabla_peliculas()

# Ejecutar la aplicación
main()
