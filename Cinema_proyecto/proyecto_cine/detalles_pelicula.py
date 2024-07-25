import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import webbrowser
import sqlite3
import login
from registrar_asientos import mostrar_registro_asientos
from colores import *
from eventos import bind_hover_events

def mostrar_detalles_pelicula(cuerpo_principal, pelicula_id, usuario_id=None):
    """
    Muestra los detalles de una película en un contenedor principal.

    Args:
        cuerpo_principal (tk.Frame): El marco donde se mostrarán los detalles de la película.
        pelicula_id (int): El ID de la película en la base de datos.
        usuario_id (int, optional): El ID del usuario que está viendo los detalles. Por defecto es None.
    """
    # Conexión a la base de datos
    conn = sqlite3.connect('cartelera.db')
    cursor = conn.cursor()

    # Obtener detalles de la película por su ID, incluyendo horarios y salas
    cursor.execute('''
        SELECT p.titulo, p.genero, p.duracion, p.imagen, p.sinopsis, GROUP_CONCAT(h.horario) AS horario, GROUP_CONCAT(h.sala) AS sala
        FROM peliculas p
        LEFT JOIN horarios h ON p.id = h.id_pelicula
        WHERE p.id=?
        GROUP BY p.titulo, p.genero, p.duracion, p.imagen, p.sinopsis
    ''', (pelicula_id,))
    pelicula = cursor.fetchone()

    # Cerrar conexión a la base de datos
    conn.close()

    # Limpiar el contenedor principal
    for widget in cuerpo_principal.winfo_children():
        widget.destroy()

    cuerpo_principal.frame_salas_actual = None

    try:
        # Cargar la imagen de la película
        imagen = Image.open(pelicula[3])
        # Ajustar el tamaño de la imagen para que ocupe una buena parte de la pantalla
        screen_width = cuerpo_principal.winfo_screenwidth()
        screen_height = cuerpo_principal.winfo_screenheight()
        imagen_resized = imagen.resize((int(screen_width * 0.4), int(screen_height * 0.7)))
        imagen_tk = ImageTk.PhotoImage(imagen_resized)
    except IOError as e:
        print("Error al cargar la imagen:", e)
        return

    # Configurar el contenedor principal
    cuerpo_principal.configure(bg=color_fondo, padx=20, pady=20)

    # Crear el marco izquierdo para los detalles principales de la película
    frame_izquierdo = tk.Frame(cuerpo_principal, bg=color_fondo)
    frame_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, padx=40, pady=10, expand=True)

    # Mostrar la imagen de la película
    label_imagen = tk.Label(frame_izquierdo, image=imagen_tk, bg=color_fondo)
    label_imagen.image = imagen_tk
    label_imagen.pack(pady=(0, 10), expand=True)

    # Mostrar el título de la película
    label_titulo = tk.Label(frame_izquierdo, text=pelicula[0], font=(fuente_personalizada[0], 20, "bold"), fg=color_titulo, bg=color_fondo)
    label_titulo.pack(pady=(0, 10), expand=True)

    # Mostrar el género de la película
    label_genero = tk.Label(frame_izquierdo, text=f"Género: {pelicula[1]}", font=(fuente_personalizada[0], 14), fg=color_texto, bg=color_fondo)
    label_genero.pack(pady=(0, 5), expand=True)

    # Mostrar la duración de la película
    label_duracion = tk.Label(frame_izquierdo, text=f"Duración: {pelicula[2]}", font=(fuente_personalizada[0], 14), fg=color_texto, bg=color_fondo)
    label_duracion.pack(pady=(0, 5), expand=True)

    try:
        # Botón para ver el tráiler de la película
        button_trailer = tk.Button(frame_izquierdo, text="Ver trailer", fg=COLOR_TEXTO_NORMAL, bg=COLOR_BOTON_NORMAL, font=fuente_personalizada, bd=2, relief="groove", command=lambda: webbrowser.open("https://www.youtube.com/watch?v=CpXJHWSXJW0"))
        button_trailer.pack(pady=(10, 20), expand=True)
        bind_hover_events(button_trailer)
    except Exception as e:
        print("Error al abrir el enlace del tráiler:", e)

    # Crear el marco derecho para la sinopsis y los horarios
    frame_derecho = tk.Frame(cuerpo_principal, bg=color_fondo)
    frame_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Mostrar la sinopsis de la película
    label_sinopsis = tk.Label(frame_derecho, text="Sinopsis:", font=(fuente_personalizada[0], 18, "bold"), fg=color_titulo, bg=color_fondo)
    label_sinopsis.pack(pady=(10, 15), anchor='w')

    sinopsis_texto = pelicula[4]
    label_sinopsis_contenido = tk.Label(frame_derecho, text=sinopsis_texto, wraplength=int(screen_width * 0.5), justify="left", font=(fuente_personalizada[0], 16), fg=color_texto, bg=color_fondo)
    label_sinopsis_contenido.pack(pady=(0, 20), anchor='w')

    if pelicula[5] is not None and pelicula[6] is not None:
        # Mostrar el título "Horarios"
        label_horarios = tk.Label(frame_derecho, text="Horarios:", font=(fuente_personalizada[0], 16, "bold"), fg=color_titulo, bg=color_fondo)
        label_horarios.pack(pady=(0, 10), anchor='w')

        # Crear el marco para los horarios
        frame_horarios = tk.Frame(frame_derecho, bg=color_fondo)
        frame_horarios.pack(pady=(10, 10))

        # Este marco contendrá los botones adicionales
        frame_botones_adicionales = tk.Frame(frame_derecho, bg=color_fondo)
        frame_botones_adicionales.pack(pady=(10, 10))

        def mostrar_botones_adicionales(cuerpo_principal, pelicula_id, horario, sala, usuario_id=None):
            """
            Muestra los botones adicionales para seleccionar la sala.

            Args:
                cuerpo_principal (tk.Frame): El marco principal.
                pelicula_id (int): El ID de la película.
                horario (str): El horario de la película.
                sala (str): La sala donde se proyecta la película.
                usuario_id (int, optional): El ID del usuario. Por defecto es None.
            """
            # Limpiar el contenido del frame_botones_adicionales
            for widget in frame_botones_adicionales.winfo_children():
                widget.destroy()

            # Crear y mostrar el botón adicional
            boton_adicional = tk.Button(frame_botones_adicionales, text=sala, fg="#FFFFFF", bg="#FF5722", font=fuente_personalizada, bd=2, relief="groove", command=lambda: mostrar_registro_asientos(cuerpo_principal, pelicula_id, horario, sala, login.usuario_id_global))
            boton_adicional.pack(side=tk.TOP, padx=5, pady=5)

            cuerpo_principal.frame_salas_actual = frame_botones_adicionales

        # Convertir las cadenas de horarios y salas en listas separadas
        horarios = pelicula[5].split(',')
        salas = pelicula[6].split(',')

        # Crear botones para cada horario y sala
        for i in range(len(horarios)):
            horario = horarios[i].strip()
            sala = salas[i].strip()
            button_horario = tk.Button(frame_horarios, text=horario, fg=COLOR_TEXTO_NORMAL, bg=COLOR_BOTON_NORMAL, font=fuente_personalizada, bd=2, relief="groove", command=lambda h=horario, s=sala: mostrar_botones_adicionales(cuerpo_principal, pelicula_id, h, s, usuario_id))
            button_horario.pack(side=tk.LEFT, padx=(5, 10))
            bind_hover_events(button_horario)

        cuerpo_principal.frame_salas_actual = frame_botones_adicionales










