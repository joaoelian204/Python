import tkinter as tk
from tkinter import font
from config import *
import util.util_ventana as util_ventana
import util.util_imagenes as util_img

def leer_imagen(path, size):
    from PIL import Image, ImageTk
    return ImageTk.PhotoImage(Image.open(path).resize(size, Image.LANCZOS))

def configurar_ventana(root):
    root.title("CINE GUI")
    w, h = 1024, 600
    util_ventana.centrar_ventana(root, w, h)

def crear_paneles(root):
    barra_superior = tk.Frame(root, bg=COLOR_BARRA_SUPERIOR, height=50)
    barra_superior.pack(side=tk.TOP, fill='both')

    menu_lateral = tk.Frame(root, bg=COLOR_MENU_LATERAL, width=150)
    menu_lateral.pack(side=tk.LEFT, fill='both', expand=False)

    cuerpo_principal = tk.Frame(root, bg=COLOR_CUERPO_PRINCIPAL)
    cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)

    return barra_superior, menu_lateral, cuerpo_principal

def configurar_barra_superior(barra_superior, toggle_panel_callback):
    font_awesome = font.Font(family='FontAwesome', size=12)

    # Etiqueta de título
    label_titulo = tk.Label(barra_superior, text="CINE GUI")
    label_titulo.config(fg="#fff", font=("Roboto", 15), bg=COLOR_BARRA_SUPERIOR, pady=10, width=16)
    label_titulo.pack(side=tk.LEFT)

    # Botón de menú lateral
    button_menu_lateral = tk.Button(barra_superior, text="\uf0c9", font=font_awesome,
                                    command=toggle_panel_callback, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white")
    button_menu_lateral.pack(side=tk.LEFT)

    # Etiqueta de información
    label_info = tk.Label(barra_superior, text="CINE GUI.com")
    label_info.config(fg="#fff", font=("Roboto", 10), bg=COLOR_BARRA_SUPERIOR, padx=10, width=20)
    label_info.pack(side=tk.RIGHT)

def configurar_menu_lateral(menu_lateral, perfil):
    ancho_menu = 20
    alto_menu = 2
    font_awesome = font.Font(family='FontAwesome', size=15)

    # Etiqueta de perfil
    label_perfil = tk.Label(menu_lateral, image=perfil, bg=COLOR_MENU_LATERAL)
    label_perfil.pack(side=tk.TOP, pady=10)

    # Botones del menú lateral
    buttons_info = [
        ("Dashboard", "\uf109"),
        ("Profile", "\uf007"),
        ("Picture", "\uf03e"),
        ("Info", "\uf129"),
        ("Settings", "\uf013")
    ]

    buttons = []
    for txt, icon in buttons_info:
        button = tk.Button(menu_lateral)
        configurar_boton_menu(button, txt, icon, font_awesome, ancho_menu, alto_menu)
        buttons.append(button)

def configurar_boton_menu(button, txt, icon, font_awesome, ancho_menu, alto_menu):
    button.config(text=f"{icon} {txt}", anchor="w", font=font_awesome,
                bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=ancho_menu, height=alto_menu)
    button.pack(side=tk.TOP)
    bind_hover_events(button)

def bind_hover_events(button):
    button.bind("<Enter>", lambda event: on_enter(event, button))
    button.bind("<Leave>", lambda event: on_leave(event, button))

def on_enter(event, button):
    button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg="white")

def on_leave(event, button):
    button.config(bg=COLOR_MENU_LATERAL, fg="white")

def toggle_panel(menu_lateral):
    if menu_lateral.winfo_ismapped():
        menu_lateral.pack_forget()
    else:
        menu_lateral.pack(side=tk.LEFT, fill="y")

def configurar_cuerpo_principal(cuerpo_principal, logo):
    label = tk.Label(cuerpo_principal, image=logo, bg=COLOR_CUERPO_PRINCIPAL)
    label.place(x=0, y=0, relwidth=1, relheight=1)

def main():
    root = tk.Tk()

    # Cargar imágenes
    logo = leer_imagen("/home/joaoelian/Escritorio/Python/DISEÑO_TK/imagenes/logocine.png", (560, 136))
    perfil = leer_imagen("/home/joaoelian/Escritorio/Python/DISEÑO_TK/imagenes/perfil.png", (100, 100))

    # Configurar ventana
    configurar_ventana(root)

    # Crear paneles
    barra_superior, menu_lateral, cuerpo_principal = crear_paneles(root)

    # Configurar barra superior
    configurar_barra_superior(barra_superior, lambda: toggle_panel(menu_lateral))

    # Configurar menú lateral
    configurar_menu_lateral(menu_lateral, perfil)

    # Configurar cuerpo principal
    configurar_cuerpo_principal(cuerpo_principal, logo)

    root.mainloop()

if __name__ == "__main__":
    main()
