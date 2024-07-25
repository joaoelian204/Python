import tkinter as tk
import sqlite3
from PIL import Image, ImageTk
from itertools import cycle
from detalles_pelicula import mostrar_detalles_pelicula
from imagenes import leer_imagen
from eventos import bind_hover_events
from colores import COLOR_BOTON_NORMAL, COLOR_TEXTO_NORMAL, COLOR_CUERPO_PRINCIPAL

def cargar_cartelera(cuerpo_principal):
    # Mostrar la publicidad
    mostrar_publicidad(cuerpo_principal)

    conn = sqlite3.connect('cartelera.db')
    cursor = conn.cursor()

    # Ejecutar consulta para obtener todas las películas de la tabla 'peliculas'
    cursor.execute('SELECT id, titulo, genero, duracion, imagen FROM peliculas')
    peliculas = cursor.fetchall()

    row_count = 1  # Iniciar desde la fila 1 para dejar la fila 0 para la publicidad
    column_count = 0
    max_columns = 5
    padding_x = 20
    padding_y = 20

    # Lista para almacenar los botones de ver más
    botones_ver_mas = []

    for pelicula in peliculas:
        # Crear un marco para cada película
        frame_pelicula = tk.Frame(cuerpo_principal, bg=COLOR_BOTON_NORMAL, highlightbackground="black", highlightthickness=2)
        frame_pelicula.grid(row=row_count, column=column_count, padx=padding_x, pady=padding_y, sticky="nsew")

        # Mostrar la imagen de la película si está disponible
        if pelicula[4]:
            imagen = leer_imagen(pelicula[4], (330, 330))
            label_imagen = tk.Label(frame_pelicula, image=imagen, bg=COLOR_CUERPO_PRINCIPAL)
            label_imagen.image = imagen
            label_imagen.pack()

        # Mostrar título de la película
        label_titulo = tk.Label(frame_pelicula, text=pelicula[1], font=("Roboto", 10, "bold"), bg=COLOR_BOTON_NORMAL, fg=COLOR_TEXTO_NORMAL)
        label_titulo.pack()

        # Mostrar género de la película
        label_genero = tk.Label(frame_pelicula, text=f"Género: {pelicula[2]}", font=("Roboto", 10), bg=COLOR_BOTON_NORMAL, fg=COLOR_TEXTO_NORMAL)
        label_genero.pack()

        # Mostrar duración de la película
        label_duracion = tk.Label(frame_pelicula, text=f"Duración: {pelicula[3]}", font=("Roboto", 10), bg=COLOR_BOTON_NORMAL, fg=COLOR_TEXTO_NORMAL)
        label_duracion.pack()

        # Botón para ver más detalles de la película
        button_ver_mas = tk.Button(frame_pelicula, text="Ver más", font=("Arial", 10, "bold"), bg=COLOR_BOTON_NORMAL, fg=COLOR_TEXTO_NORMAL, bd=0,
                            command=lambda id_pelicula=pelicula[0]: mostrar_detalles_pelicula(cuerpo_principal, id_pelicula))
        button_ver_mas.pack(pady=7, padx=10)

        botones_ver_mas.append(button_ver_mas)

        # Incrementar contador de columnas y filas
        column_count += 1
        if column_count >= max_columns:
            column_count = 0
            row_count += 1

    # Asegurar que las filas se muestran incluso si no están completas
    if column_count != 0:
        for empty_column in range(column_count, max_columns):
            frame_placeholder = tk.Frame(cuerpo_principal, bg=COLOR_CUERPO_PRINCIPAL, highlightbackground=COLOR_CUERPO_PRINCIPAL, highlightthickness=2)
            frame_placeholder.grid(row=row_count, column=empty_column, padx=padding_x, pady=padding_y, sticky="nsew")

    # Vincular eventos hover a todos los botones "Ver más"
    for button in botones_ver_mas:
        bind_hover_events(button)

    # Cerrar conexión y commit de cambios (aunque en este caso no se están modificando los datos)
    conn.commit()
    conn.close()

    # Crear un contenedor para el carousel de imágenes
    container_frame = tk.Frame(cuerpo_principal,bg="#f0f0f0")
    container_frame.grid(row=row_count + 1, column=0, columnspan=5, padx=20, pady=20, sticky="nsew")

    # Llamar función para mostrar el carousel de imágenes
    mostrar_carousel_imagenes(container_frame)
    
def get_publicidad_peliculas_urls():
    conn = sqlite3.connect('cartelera.db')
    cursor = conn.cursor()
    cursor.execute('SELECT url FROM publicidad_peliculas')
    urls = [row[0] for row in cursor.fetchall()]
    conn.close()
    return urls

def mostrar_publicidad(cuerpo_principal):
    # Obtener las URLs de publicidad desde la base de datos
    rutas_imagenes_publicidad = get_publicidad_peliculas_urls()
    
    # Crear una lista de objetos ImageTk.PhotoImage a partir de las URLs
    imagenes = [ImageTk.PhotoImage(Image.open(ruta).resize((1400, 400), Image.LANCZOS)) for ruta in rutas_imagenes_publicidad]
    imagenes_cycle = cycle(imagenes)
    
    # Crear un marco para la publicidad
    frame_publicidad = tk.Frame(cuerpo_principal, bg="#f0f0f0", highlightbackground="#f0f0f0", highlightthickness=2, width=2048, height=696)
    frame_publicidad.grid(row=0, column=0, columnspan=5, padx=20, pady=20, sticky="nsew")
    
    # Mostrar la primera imagen de la lista
    label_imagen_publicidad = tk.Label(frame_publicidad, bg="#f0f0f0")
    label_imagen_publicidad.pack()
    
    # Función para cambiar la imagen de la publicidad cada 5 segundos
    def actualizar_publicidad():
        try:
            imagen_publicidad = next(imagenes_cycle)
            label_imagen_publicidad.config(image=imagen_publicidad)
            label_imagen_publicidad.image = imagen_publicidad
            cuerpo_principal.after(5000, actualizar_publicidad)  # Cambiar imagen cada 5 segundos
        except tk.TclError:
            # El widget ya no existe, por lo que no hacemos nada.
            pass
        
    actualizar_publicidad()
    
def get_imagenes_publicidad_urls():
    conn = sqlite3.connect('cartelera.db')
    cursor = conn.cursor()
    cursor.execute('SELECT url FROM imagenes_publicidad')
    urls = [row[0] for row in cursor.fetchall()]
    conn.close()
    return urls

def mostrar_carousel_imagenes(container_frame):
    # Obtener las URLs de las imágenes desde la base de datos
    image_files = get_imagenes_publicidad_urls()
    
    interval = 4500  # Intervalo en milisegundos para cambiar las imágenes
    current_image = 0  # Índice de la imagen actual en la lista

    # Cargar las imágenes y redimensionarlas
    images = [ImageTk.PhotoImage(Image.open(image).resize((550, 400))) for image in image_files]

    # Crear frames para mostrar las imágenes del carousel
    frame1 = tk.Frame(container_frame, width=550, height=400, bg="#f0f0f0")
    frame2 = tk.Frame(container_frame, width=550, height=400, bg="#f0f0f0")
    frame3 = tk.Frame(container_frame, width=550, height=400, bg="#f0f0f0")

    # Posicionar los frames en la cuadrícula dentro del container_frame
    frame1.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")
    frame2.grid(row=0, column=1, padx=30, pady=30, sticky="nsew")
    frame3.grid(row=0, column=2, padx=30, pady=30, sticky="nsew")

    # Crear etiquetas para mostrar las imágenes en los frames
    label1 = tk.Label(frame1)
    label2 = tk.Label(frame2)
    label3 = tk.Label(frame3)

    # Expandir las etiquetas para llenar el espacio disponible en los frames
    label1.pack(expand=True)
    label2.pack(expand=True)
    label3.pack(expand=True)

    # Función para actualizar las imágenes en el carousel
    def update_image():
        nonlocal current_image
        label1.config(image=images[current_image])
        label2.config(image=images[(current_image + 1) % len(images)])
        label3.config(image=images[(current_image + 2) % len(images)])
        current_image = (current_image + 1) % len(images)
        container_frame.after(interval, update_image)  # Llamar recursivamente para cambiar las imágenes

    # Iniciar el carousel llamando a la función update_image
    update_image()

