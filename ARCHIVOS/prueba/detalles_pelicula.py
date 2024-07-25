import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import webbrowser

def mostrar_detalles_pelicula(cuerpo_principal, pelicula):
    """
    Muestra los detalles de una película seleccionada en el mismo cuerpo principal.

    Args:
        cuerpo_principal (tk.Frame): El marco del cuerpo principal donde se mostrarán los detalles.
        pelicula (dict): Diccionario con la información de la película.
    """
    # Limpiar el cuerpo principal
    for widget in cuerpo_principal.winfo_children():
        widget.destroy()

    # Configurar colores
    color_fondo = "#F0F0F0"
    color_titulo = "#333"
    color_texto = "#666"

    # Configurar fuente personalizada
    fuente_personalizada = "Arial"

    # Cargar y redimensionar la imagen
    imagen = Image.open(pelicula["imagen"])
    imagen_resized = imagen.resize((360, 400))
    imagen_tk = ImageTk.PhotoImage(imagen_resized)

    # Establecer el fondo del cuerpo principal
    cuerpo_principal.configure(bg=color_fondo, padx=20, pady=20)

    # Crear el marco izquierdo para la imagen y detalles
    frame_izquierdo = tk.Frame(cuerpo_principal, bg=color_fondo)
    frame_izquierdo.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=10)

    # Crear y colocar la etiqueta de la imagen
    label_imagen = tk.Label(frame_izquierdo, image=imagen_tk, bg=color_fondo)
    label_imagen.image = imagen_tk  # Guardar una referencia para evitar que la imagen se elimine inmediatamente
    label_imagen.pack(pady=(0, 20))

    # Crear y colocar la etiqueta del título
    label_titulo = tk.Label(frame_izquierdo, text=pelicula["titulo"], font=(fuente_personalizada, 18, "bold"), fg=color_titulo, bg=color_fondo)
    label_titulo.pack(pady=(0, 10))

    # Crear y colocar la etiqueta del género
    label_genero = tk.Label(frame_izquierdo, text=f"Género: {pelicula['Genero']}", font=(fuente_personalizada, 14), fg=color_texto, bg=color_fondo)
    label_genero.pack(pady=(0, 5))

    # Crear y colocar la etiqueta de la duración
    label_duracion = tk.Label(frame_izquierdo, text=f"Duración: {pelicula['Duracion']}", font=(fuente_personalizada, 14), fg=color_texto, bg=color_fondo)
    label_duracion.pack(pady=(0, 5))
    
    # Botón de ver trailer
    button_trailer = tk.Button(frame_izquierdo, text="Ver trailer", fg=color_texto, bg=color_fondo, font=("Arial", 12), bd=2, 
                            command=lambda: webbrowser.open("https://www.youtube.com/watch?v=CpXJHWSXJW0"))
    button_trailer.pack(pady=(10, 20))

    
    # Crear el marco derecho para la sinopsis y horarios
    frame_derecho = tk.Frame(cuerpo_principal, bg=color_fondo)
    frame_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10,)

    # Crear y colocar la etiqueta de la sinopsis
    label_sinopsis = tk.Label(frame_derecho, text="Sinopsis:", font=(fuente_personalizada, 16, "bold"), fg=color_titulo, bg=color_fondo)
    label_sinopsis.pack(pady=(10, 15), anchor='w')

    sinopsis_texto = pelicula["sinopsis"]
    label_sinopsis_contenido = tk.Label(frame_derecho, text=sinopsis_texto, wraplength=500, justify="left", font=(fuente_personalizada, 12), fg=color_texto, bg=color_fondo)
    label_sinopsis_contenido.pack(pady=(0, 20), anchor='w')

    # Crear y colocar la etiqueta de los horarios
    label_horarios = tk.Label(frame_derecho, text="Horarios:", font=(fuente_personalizada, 16, "bold"), fg=color_titulo, bg=color_fondo)
    label_horarios.pack(pady=(0, 10), anchor='w')

    horarios_texto = pelicula["horarios"]
    label_horarios_contenido = tk.Label(frame_derecho, text=horarios_texto, wraplength=500, justify="left", font=(fuente_personalizada, 12), fg=color_texto, bg=color_fondo)
    label_horarios_contenido.pack(pady=(0, 20), anchor='w')

    