import tkinter as tk
from configuracion import configurar_ventana, crear_paneles, configurar_barra_superior, configurar_menu_lateral
from cargar_cartelera import cargar_cartelera 
from eventos import toggle_panel 
from login import mostrar_login  

def main():
    root = tk.Tk()  # Crea una instancia de la clase Tk para la ventana principal

    def on_login_success():
        configurar_ventana(root)  # Configura la ventana principal
        barra_superior, menu_lateral, cuerpo_principal = crear_paneles(root)  # Crea los paneles de la interfaz
        configurar_barra_superior(barra_superior, lambda: toggle_panel(menu_lateral))  # Configura la barra superior
        configurar_menu_lateral(menu_lateral, cuerpo_principal, root, on_login_success)  # Configura el menú lateral
        cargar_cartelera(cuerpo_principal)  # Carga la cartelera en el cuerpo principal

    mostrar_login(root, on_login_success)
    root.mainloop() 

if __name__ == "__main__":
    main() 
