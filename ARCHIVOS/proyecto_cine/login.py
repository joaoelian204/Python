import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import registro  # Importamos el módulo de registro

# Variable global para almacenar el ID del usuario
usuario_id_global = None

def verificar_credenciales(usuario, contraseña):
    usuario_registrado = registro.verificar_credenciales(usuario, contraseña)
    if usuario_registrado:
        global usuario_id_global
        usuario_id_global = usuario_registrado[0]  # Asignar el ID del usuario a la variable global
        return True
    return False

def mostrar_login(root, on_login_success):
    root.withdraw()  # Ocultar la ventana principal mientras se muestra el login

    login_window = tk.Toplevel(root)
    login_window.title("Iniciar Sesión")
    login_window.geometry("500x750")
    login_window.resizable(False, False)
    login_window.configure(bg="#2c3e50")

    # Descargar y mostrar imagen
    imagenty = "https://img.freepik.com/vector-premium/plantilla-diseno-logotipo-pelicula-rollo-camara-cine_527727-210.jpg"
    response = requests.get(imagenty)
    imagen = Image.open(BytesIO(response.content))
    imagen = imagen.resize((200, 200), Image.LANCZOS)
    imagen = ImageTk.PhotoImage(imagen)

    label_imagen = tk.Label(login_window, image=imagen, bg="#2c3e50")
    label_imagen.image = imagen  # Mantener una referencia para evitar que la imagen sea recolectada por el garbage collector
    label_imagen.pack(pady=20)

    # Título
    label_titulo = tk.Label(login_window, text="Iniciar Sesión", font=("Arial", 24, "bold"), bg="#2c3e50", fg="#ecf0f1")
    label_titulo.pack(pady=10)

    # Usuario
    tk.Label(login_window, text="Usuario", font=("Arial", 14), bg="#2c3e50", fg="#ecf0f1").pack(pady=(40, 5))
    entry_usuario = tk.Entry(login_window, font=("Arial", 14), bd=5, relief=tk.GROOVE)
    entry_usuario.pack(pady=10, ipady=5, ipadx=10)

    # Contraseña
    tk.Label(login_window, text="Contraseña", font=("Arial", 14), bg="#2c3e50", fg="#ecf0f1").pack(pady=10)
    entry_contraseña = tk.Entry(login_window, show="*", font=("Arial", 14), bd=5, relief=tk.GROOVE)
    entry_contraseña.pack(pady=10, ipady=5, ipadx=10)

    def intentar_login():
        usuario = entry_usuario.get()
        contraseña = entry_contraseña.get()
        if verificar_credenciales(usuario, contraseña):
            login_window.destroy()
            root.deiconify()
            on_login_success()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    # Botón de inicio de sesión
    tk.Button(login_window, text="Iniciar Sesión", command=intentar_login, font=("Arial", 14), bg="#2980b9", fg="#ecf0f1", bd=0, relief=tk.FLAT, padx=10, pady=10).pack(pady=20)
    
    # Botón de registro
    tk.Button(login_window, text="Registrarse", command=registro.abrir_ventana_registro, font=("Arial", 14), bg="#2980b9", fg="#ecf0f1", bd=0, relief=tk.FLAT, padx=10, pady=10).pack(pady=10)
