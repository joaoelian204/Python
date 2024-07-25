import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk

# Definición de colores utilizados en la interfaz
COLOR_BARRA_SUPERIOR = "#333333"
COLOR_MENU_LATERAL = "#444444"
COLOR_CUERPO_PRINCIPAL = "#f0f0f0"
COLOR_MENU_CURSOR_ENCIMA = "#555555"
COLOR_BOTON_NORMAL = "#000000"
COLOR_BOTON_HOVER = "#ffffff"
COLOR_TEXTO_NORMAL = "#ffffff"
COLOR_TEXTO_HOVER = "#000000"

# FUNCIONES AUXILIARES
def leer_imagen(path, size):
    """
    Lee una imagen desde el sistema de archivos y la redimensiona al tamaño especificado.
    
    Args:
        path (str): La ruta del archivo de imagen.
        size (tuple): El tamaño al que se debe redimensionar la imagen (ancho, alto).
        
    Returns:
        ImageTk.PhotoImage: La imagen redimensionada.
    """
    return ImageTk.PhotoImage(Image.open(path).resize(size, Image.LANCZOS))

def on_enter(event, button):
    """
    Cambia el color del botón cuando el cursor está encima.

    Args:
        event (tk.Event): El evento de entrada del cursor.
        button (tk.Button): El botón al que se le aplica el cambio.
    """
    button.config(bg=COLOR_BOTON_HOVER, fg=COLOR_TEXTO_HOVER)

def on_leave(event, button):
    """
    Restaura el color original del botón cuando el cursor sale de él.

    Args:
        event (tk.Event): El evento de salida del cursor.
        button (tk.Button): El botón al que se le aplica el cambio.
    """
    button.config(bg=COLOR_BOTON_NORMAL, fg=COLOR_TEXTO_NORMAL)

def bind_hover_events(button):
    """
    Asocia eventos de hover (entrada y salida del cursor) a un botón.

    Args:
        button (tk.Button): El botón al que se le asocian los eventos.
    """
    button.bind("<Enter>", lambda event: on_enter(event, button))
    button.bind("<Leave>", lambda event: on_leave(event, button))

def toggle_panel(menu_lateral):
    """
    Muestra u oculta el menú lateral.

    Args:
        menu_lateral (tk.Frame): El marco del menú lateral que se va a mostrar u ocultar.
    """
    if menu_lateral.winfo_ismapped():
        menu_lateral.pack_forget()
    else:
        menu_lateral.pack(side=tk.LEFT, fill=tk.Y)

# CONFIGURACION DE LA VENTANA PRINCIPAL Y PANELES
def configurar_ventana(root):
    """
    Configura las propiedades principales de la ventana.

    Args:
        root (tk.Tk): La ventana principal de la aplicación.
    """
    root.title("Plataforma de Cine")
    root.geometry("1024x600")

def crear_paneles(root):
    """
    Crea y organiza los paneles principales de la interfaz.

    Args:
        root (tk.Tk): La ventana principal de la aplicación.
    
    Returns:
        tuple: Los paneles creados (barra_superior, menu_lateral, cuerpo_principal).
    """
    # Barra superior
    barra_superior = tk.Frame(root, bg=COLOR_BARRA_SUPERIOR, height=50)
    barra_superior.pack(side=tk.TOP, fill=tk.BOTH)

    # Menú lateral
    menu_lateral = tk.Frame(root, bg=COLOR_MENU_LATERAL, width=200)
    menu_lateral.pack(side=tk.LEFT, fill=tk.Y)

    # Área de contenido principal con scrollbar
    canvas = tk.Canvas(root, bg=COLOR_CUERPO_PRINCIPAL)
    canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    cuerpo_principal = tk.Frame(canvas, bg=COLOR_CUERPO_PRINCIPAL)
    canvas.create_window((0, 0), window=cuerpo_principal, anchor="nw")

    # Ajustar el área de desplazamiento del canvas
    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    cuerpo_principal.bind("<Configure>", on_configure)

    return barra_superior, menu_lateral, cuerpo_principal

# CONFIGURACION DE LA BARRA SUPERIOR Y MENU LATERAL
def configurar_barra_superior(barra_superior, toggle_panel_callback):
    """
    Configura los elementos de la barra superior.

    Args:
        barra_superior (tk.Frame): El marco de la barra superior.
        toggle_panel_callback (function): La función que se llamará al hacer clic en el botón del menú lateral.
    """
    font_awesome = font.Font(family='FontAwesome', size=15)

    label_titulo = tk.Label(barra_superior, text="Plataforma de Cine", fg="#fff", font=("Roboto", 15), bg=COLOR_BARRA_SUPERIOR, pady=10,highlightthickness=0)
    label_titulo.pack(side=tk.LEFT, padx=10)

    button_menu_lateral = tk.Button(barra_superior, text="☰", font=font_awesome, command=toggle_panel_callback, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="#fff", padx=10)
    button_menu_lateral.pack(side=tk.LEFT, padx=10)

    label_info = tk.Label(barra_superior, text="PlataformaDeCine.com", fg="#fff", font=("Roboto", 10), bg=COLOR_BARRA_SUPERIOR, padx=10)
    label_info.pack(side=tk.RIGHT)

def configurar_menu_lateral(menu_lateral):
    """
    Configura los botones del menú lateral.

    Args:
        menu_lateral (tk.Frame): El marco del menú lateral.
    """
    font_awesome = font.Font(family='FontAwesome', size=15)

    buttons_info = [
        ("Cartelera", "🎬"),
        ("Próximamente", "📅"),
        ("Mi Perfil", "👤"),
        ("Cerrar Sesión", "🚪")
    ]

    for txt, icon in buttons_info:
        button = tk.Button(menu_lateral, text=f"{icon} {txt}", anchor="w", font=("Arial", 12), bd=0, bg=COLOR_MENU_LATERAL, fg="#fff", width=15, height=1)
        button.pack(side=tk.TOP, pady=10, padx=20, fill=tk.X)
        bind_hover_events(button)

# CARGAR CARTELERA
def cargar_cartelera(cuerpo_principal):
    """
    Carga la información de las películas en el área principal.

    Args:
        cuerpo_principal (tk.Frame): El marco del cuerpo principal donde se mostrarán las películas.
    """
    peliculas = [
        {"titulo": "Bohemian Rhapsody", "Genero": "Biografía/Drama", "Duracion": "2h 14min", "imagen": "/home/joaoelian/Descargas/bohemian_rhapsody.jpg"},
        {"titulo": "Avatar", "Genero": "Ciencia ficción", "Duracion": "2h 42min", "imagen": "/home/joaoelian/Descargas/avatar.jpg"},
        {"titulo": "Back to the Future", "Genero": "Ciencia ficción/\nAventura", "Duracion": "1h 56min", "imagen": "/home/joaoelian/Descargas/back_to_the_future.jpg"},
        {"titulo": "The Godfather", "Genero": "Crimen/Drama", "Duracion": "2h 55min", "imagen": "/home/joaoelian/Descargas/the_godfather.jpg"},
        {"titulo": "The Shawshank\nRedemption", "Genero": "Drama", "Duracion": "2h 22min", "imagen": "/home/joaoelian/Descargas/redemption.jpg"},
        {"titulo": "The Dark Knight", "Genero": "Acción/Crimen", "Duracion": "2h 32min", "imagen": "/home/joaoelian/Descargas/the_Dark_Knight.jpg"},
        {"titulo": "Inception", "Genero": "Acción/Aventura", "Duracion": "2h 28min", "imagen": "/home/joaoelian/Descargas/inception.jpg"},
        {"titulo": "Interstellar", "Genero": "Aventura/Drama", "Duracion": "2h 49min", "imagen": "/home/joaoelian/Descargas/interstellar.jpg"},
    ]

    row_count = 0
    column_count = 0
    max_columns = 4
    padding_x = 20
    padding_y = 20

    for pelicula in peliculas:
        # Crear una etiqueta para la película
        label_pelicula = tk.Label(cuerpo_principal, text=pelicula["titulo"], font=("Roboto", 10), bg=COLOR_BOTON_NORMAL, fg=COLOR_TEXTO_NORMAL, bd=0, highlightbackground="black", highlightthickness=2)
        label_pelicula.grid(row=row_count, column=column_count, padx=padding_x, pady=padding_y, sticky="nsew")
        
        if "imagen" in pelicula:
            imagen = leer_imagen(pelicula["imagen"], (150, 150))
            label_imagen = tk.Label(label_pelicula, image=imagen, bg=COLOR_CUERPO_PRINCIPAL)
            label_imagen.image = imagen
            label_imagen.pack()

        label_titulo = tk.Label(label_pelicula, text=pelicula["titulo"], font=("Roboto", 10, "bold"), bg=COLOR_BOTON_NORMAL, fg=COLOR_TEXTO_NORMAL)
        label_titulo.pack()

        label_genero = tk.Label(label_pelicula, text=f"Género: {pelicula['Genero']}", font=("Roboto", 10), bg=COLOR_BOTON_NORMAL, fg=COLOR_TEXTO_NORMAL)
        label_genero.pack()

        label_duracion = tk.Label(label_pelicula, text=f"Duración: {pelicula['Duracion']}", font=("Roboto", 10), bg=COLOR_BOTON_NORMAL, fg=COLOR_TEXTO_NORMAL)
        label_duracion.pack()

        column_count += 1
        if column_count >= max_columns:
            column_count = 0
            row_count += 1
                # Botón "Ver más"
        button_ver_mas = tk.Button(label_pelicula, text="Ver más", font=("Arial", 10, "bold"), bg=COLOR_BOTON_NORMAL, fg=COLOR_TEXTO_NORMAL, bd=0)
        button_ver_mas.pack(pady=7, padx=10)

        bind_hover_events(button_ver_mas)

# INICIALIZACION DE LA APLICACION
def main():
    """
    Función principal que inicializa y ejecuta la aplicación.
    """
    root = tk.Tk()

    configurar_ventana(root)
    barra_superior, menu_lateral, cuerpo_principal = crear_paneles(root)
    configurar_barra_superior(barra_superior, lambda: toggle_panel(menu_lateral))
    configurar_menu_lateral(menu_lateral)
    cargar_cartelera(cuerpo_principal)

    root.mainloop()

if __name__ == "__main__":
    main()
