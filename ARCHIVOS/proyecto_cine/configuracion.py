import tkinter as tk
import sys
from tkinter import font, messagebox
from eventos import toggle_panel, bind_hover_events
from cargar_cartelera import cargar_cartelera
from colores import *
from usuario_info import mostrar_perfil
from tkinter import ttk
from login import mostrar_login  # Importar la función de login desde login.py


def configurar_ventana(root):
    """
    Configura la ventana principal del aplicativo.

    Args:
        root (tk.Tk): La ventana principal de la aplicación.
    """
    root.title("Plataforma de Cine")  # Establece el título de la ventana
    root.geometry("1920x1010")  # Establece el tamaño de la ventana
    root.resizable(False, False)  # Deshabilita la opción de redimensionar la ventana

def crear_paneles(root):
    """
    Crea y configura los paneles principales de la interfaz.

    Args:
        root (tk.Tk): La ventana principal de la aplicación.

    Returns:
        tuple: Los frames barra_superior, menu_lateral y cuerpo_principal.
    """
    # Crear la barra superior
    barra_superior = tk.Frame(root, bg=COLOR_BARRA_SUPERIOR, height=50)
    barra_superior.pack(side=tk.TOP, fill=tk.BOTH)  # Empaquetar en la parte superior y llenar en ambos sentidos

    # Crear el menú lateral
    menu_lateral = tk.Frame(root, bg=COLOR_MENU_LATERAL, width=200)
    menu_lateral.pack(side=tk.LEFT, fill=tk.Y)  # Empaquetar en el lado izquierdo y llenar en el eje Y

    # Crear el canvas para el cuerpo principal con capacidad de desplazamiento
    canvas = tk.Canvas(root, bg=COLOR_CUERPO_PRINCIPAL)
    canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)  # Empaquetar en el lado derecho y llenar ambos sentidos, expandiéndose

    # Crear el frame principal dentro del canvas
    cuerpo_principal = tk.Frame(canvas, bg=COLOR_CUERPO_PRINCIPAL)
    canvas.create_window((0, 0), window=cuerpo_principal, anchor="nw")  # Crear una ventana dentro del canvas

    # Crear la scrollbar vertical para el canvas (personalizada con ttk)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Empaquetar en el lado derecho y llenar en el eje Y

    # Configurar el estilo del scrollbar
    style = ttk.Style()
    style.theme_use("alt")  # Cambiar al tema "alt"
    style.configure("Vertical.TScrollbar", gripcount=0, troughcolor="#f0f0f0", bordercolor="#f0f0f0",
                    arrowsize=12, width=10, sliderlength=30, sliderrelief="flat", sliderborderwidth=0)

    # Aplicar el estilo al scrollbar
    scrollbar.configure(style="Vertical.TScrollbar")

    # Configurar el scrollbar para el canvas
    canvas.configure(yscrollcommand=scrollbar.set)

    # Función para ajustar el scrollregion cuando cambia el tamaño del contenido
    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    cuerpo_principal.bind("<Configure>", on_configure)  # Vincular la configuración del frame principal al evento

    # Habilitar scroll con la rueda del ratón en cualquier parte de la ventana
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    root.bind_all("<MouseWheel>", on_mousewheel)  # Vincular el scroll del ratón a la ventana

    return barra_superior, menu_lateral, cuerpo_principal

def configurar_barra_superior(barra_superior, toggle_panel_callback):
    """
    Configura los elementos de la barra superior.

    Args:
        barra_superior (tk.Frame): El frame de la barra superior.
        toggle_panel_callback (function): Función para alternar el panel lateral.
    """
    font_awesome = font.Font(family='FontAwesome', size=15)  # Fuente para el botón de menú

    # Etiqueta del título
    label_titulo = tk.Label(barra_superior, text="Cinema", fg="#fff", font=("Roboto", 20), bg=COLOR_BARRA_SUPERIOR, pady=10, highlightthickness=0)
    label_titulo.pack(side=tk.LEFT, padx=10)  # Empaquetar a la izquierda con un padding

    # Botón del menú lateral
    button_menu_lateral = tk.Button(barra_superior, text="☰", font=font_awesome, command=toggle_panel_callback, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="#fff", padx=10)
    button_menu_lateral.pack(side=tk.LEFT, padx=10)  # Empaquetar a la izquierda con un padding

    # Etiqueta de información del usuario
    label_info = tk.Label(barra_superior, text="HOLA BIENVENIDO", fg="#fff", font=("Roboto", 13), bg=COLOR_BARRA_SUPERIOR, padx=10)
    label_info.pack(side=tk.RIGHT)  # Empaquetar a la derecha

def mostrar_cartelera(cuerpo_principal):
    """
    Muestra la cartelera de películas en el cuerpo principal.

    Args:
        cuerpo_principal (tk.Frame): El frame principal donde se mostrará la cartelera.
    """
    for widget in cuerpo_principal.winfo_children():
        widget.destroy()  # Eliminar todos los widgets del frame principal
    
    cargar_cartelera(cuerpo_principal)  # Cargar la cartelera en el frame principal
    
def cerrar_sesion():
    # Mostrar un mensaje de confirmación
    if messagebox.askokcancel("Cerrar programa", "¿Estás seguro que deseas cerrar sesion?"):
        # Cerrar el programa
        sys.exit()

def configurar_menu_lateral(menu_lateral, cuerpo_principal, root, on_login_success):
    """
    Configura los elementos del menú lateral.

    Args:
        menu_lateral (tk.Frame): El frame del menú lateral.
        cuerpo_principal (tk.Frame): El frame principal de la aplicación.
        root (tk.Tk): La ventana principal de la aplicación.
        on_login_success (function): Función a ejecutar al iniciar sesión correctamente.
    """
        
    font_awesome = font.Font(family='FontAwesome', size=15)  # Fuente para los botones del menú lateral
    from producto_comida import mostrar_comida  # Importar la función mostrar_comida desde py.py
    # Información del usuario
    usuario = {
        "nombre": "Joao",
        "imagen": "/home/joaoelian/Descargas/RickMorty-removebg-preview.png",
        "apellido": "Moreira",
        "correo": "joaoM@example.com",
        "pais": "Ecuador",
        "provincia": "Manabi",
        "ciudad": "Manta",
        "cedula": "123456789"
    }

    # Información de los botones del menú lateral
    buttons_info = [
        ("Cartelera", "🎬", lambda: mostrar_cartelera(cuerpo_principal)),  # Botón para mostrar la cartelera
        ("Mi Perfil", "👤", lambda: mostrar_perfil(cuerpo_principal, usuario)), 
        ("Comida", "🍔", lambda: mostrar_comida(cuerpo_principal)),# Botón para mostrar el perfil del usuario
        ("Cerrar Sesión", "🚪", lambda:cerrar_sesion())  # Botón para cerrar sesión
    ]

    # Crear botones para el menú lateral
    for txt, icon, command in buttons_info:
        button = tk.Button(menu_lateral, text=f"{icon} {txt}", anchor="w", font=font_awesome, bd=0, bg=COLOR_BOTON_NORMAL, fg="#fff", width=15, height=1, command=command)
        button.pack(side=tk.TOP, pady=10, padx=20, fill=tk.X)  # Empaquetar cada botón en el menú lateral
        bind_hover_events(button)  # Vincular eventos de hover a cada botón



