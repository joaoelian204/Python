# ui.py
import tkinter as tk
from tkinter import font
from info_usuario import *
from funciones import toggle_panel, mostrar_cartelera, mostrar_ventana_agregar
from publicidad import gestionar_publicidad  # Importar la función de publicidad
from gestor_productos import mostrar_productos

def iniciar_aplicacion():
    """
    Inicializa y ejecuta la aplicación principal de la plataforma de cine.
    """
    root = tk.Tk()  # Crea la ventana principal de la aplicación
    configurar_ventana(root)  # Configura las propiedades de la ventana

    # Crea y configura los paneles de la aplicación
    barra_superior, menu_lateral, cuerpo_principal = crear_paneles(root)
    configurar_barra_superior(barra_superior, lambda: toggle_panel(menu_lateral))
    configurar_menu_lateral(menu_lateral, cuerpo_principal)

    # Muestra la cartelera en el cuerpo principal de la aplicación
    mostrar_cartelera(cuerpo_principal)

    root.mainloop()  # Inicia el bucle principal de la aplicación

def configurar_ventana(root):
    """
    Configura las propiedades de la ventana principal de la aplicación.

    Parámetros:
        root (tk.Tk): La ventana principal de la aplicación.
    """
    root.title("Plataforma de Cine")  # Establece el título de la ventana
    root.geometry("1920x1010")  # Establece el tamaño de la ventana
    root.resizable(False, False)  # Desactiva la redimensión de la ventana

def crear_paneles(root):
    """
    Crea y configura los paneles de la ventana principal.

    Parámetros:
        root (tk.Tk): La ventana principal de la aplicación.

    Retorna:
        tuple: Una tupla que contiene los widgets de la barra superior, el menú lateral y el cuerpo principal.
    """
    from constants import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL

    # Crea la barra superior
    barra_superior = tk.Frame(root, bg=COLOR_BARRA_SUPERIOR, height=50)
    barra_superior.pack(side=tk.TOP, fill=tk.BOTH)

    # Crea el menú lateral
    menu_lateral = tk.Frame(root, bg=COLOR_MENU_LATERAL, width=200)
    menu_lateral.pack(side=tk.LEFT, fill=tk.Y)

    # Crea el canvas para el cuerpo principal con un scrollbar
    canvas = tk.Canvas(root, bg=COLOR_CUERPO_PRINCIPAL)
    canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    # Crea el frame dentro del canvas para el contenido principal
    cuerpo_principal = tk.Frame(canvas, bg=COLOR_CUERPO_PRINCIPAL)
    canvas.create_window((0, 0), window=cuerpo_principal, anchor="nw")

    # Ajusta la región de scroll del canvas
    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    cuerpo_principal.bind("<Configure>", on_configure)

    return barra_superior, menu_lateral, cuerpo_principal

def configurar_barra_superior(barra_superior, toggle_panel_callback):
    """
    Configura la barra superior de la aplicación.

    Parámetros:
        barra_superior (tk.Frame): El frame que representa la barra superior.
        toggle_panel_callback (func): La función que se ejecutará para alternar el menú lateral.
    """
    from constants import COLOR_BARRA_SUPERIOR
    font_awesome = font.Font(family='FontAwesome', size=15)  # Fuente para íconos

    # Label del título
    label_titulo = tk.Label(barra_superior, text="Plataforma Administrador Cine", fg="#fff", font=("Roboto", 15), bg=COLOR_BARRA_SUPERIOR, pady=10, highlightthickness=0)
    label_titulo.pack(side=tk.LEFT, padx=10)

    # Botón para alternar el menú lateral
    button_menu_lateral = tk.Button(barra_superior, text="☰", font=font_awesome, command=toggle_panel_callback, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="#fff", padx=10)
    button_menu_lateral.pack(side=tk.LEFT, padx=10)

    # Label de información
    label_info = tk.Label(barra_superior, text="BIENVENIDO ADMIM", fg="#fff", font=("Roboto", 13), bg=COLOR_BARRA_SUPERIOR, padx=10)
    label_info.pack(side=tk.RIGHT)

def configurar_menu_lateral(menu_lateral, cuerpo_principal):
    """
    Configura el menú lateral de la aplicación.

    Parámetros:
        menu_lateral (tk.Frame): El frame que representa el menú lateral.
        cuerpo_principal (tk.Frame): El frame principal donde se mostrará el contenido.
    """
    font_awesome = font.Font(family='FontAwesome', size=15)  # Fuente para íconos
    buttons_info = [
        ("Editar Película", "🎬", lambda: mostrar_cartelera(cuerpo_principal)),
        ("Añadir Película", "➕", lambda: mostrar_ventana_agregar(cuerpo_principal)),
        ("Ver Usuario", "👤", lambda: mostrar_ventana_usuarios()), 
        ("Ver Publicidad", "📺", gestionar_publicidad),
        ("Editar Producto", "🛒", lambda: mostrar_productos(cuerpo_principal)),  # Añadir botón para gestor de productos
    ]
    from constants import COLOR_BOTON_NORMAL
    for txt, icon, command in buttons_info:
        # Crea y configura cada botón del menú lateral
        button = tk.Button(menu_lateral, text=f"{icon} {txt}", anchor="w", font=font_awesome, bd=0, bg=COLOR_BOTON_NORMAL, fg="#fff", width=17, height=1, command=command)
        button.pack(side=tk.TOP, pady=10, padx=20, fill=tk.X)  # Coloca el botón en el menú lateral



