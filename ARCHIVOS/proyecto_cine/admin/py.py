import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randint
import tkinter as tk
from tkinter import messagebox

# Configuración del servidor SMTP
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
correo = 'joaoelian24@gmail.com'  # Reemplaza con tu correo
password = 'cupl jlmm ixto zshh'  # Reemplaza con tu contraseña

# Base de datos temporal de usuarios
usuarios_temporales = {}
usuarios_registrados = {}

def enviar_correo_verificacion(destinatario, codigo_verificacion):
    usuario = 'Elian'
    asunto = 'Verificación de correo'
    mensaje = f'Hola, tu código de verificación es: {codigo_verificacion}'
    
    msg = MIMEMultipart()
    msg['From'] = usuario
    msg['Subject'] = asunto
    msg['To'] = ', '.join(destinatario)
    msg.attach(MIMEText(mensaje))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(correo, password)
        server.sendmail(usuario, destinatario, msg.as_string())
        print('Correo enviado exitosamente')

def register_user(email, username, password):
    if email in usuarios_registrados:
        messagebox.showerror("Error", "El correo ya está registrado.")
        return False

    codigo_verificacion = randint(100000, 999999)
    usuarios_temporales[email] = {
        'username': username,
        'password': password,
        'codigo_verificacion': codigo_verificacion
    }
    
    enviar_correo_verificacion([email], codigo_verificacion)
    messagebox.showinfo("Registro", "Usuario registrado temporalmente. Verifica tu correo.")
    return True

def verify_email(email, codigo_verificacion):
    if email in usuarios_temporales and usuarios_temporales[email]['codigo_verificacion'] == codigo_verificacion:
        usuarios_registrados[email] = {
            'username': usuarios_temporales[email]['username'],
            'password': usuarios_temporales[email]['password']
        }
        del usuarios_temporales[email]
        messagebox.showinfo("Verificación", "Correo verificado y usuario registrado exitosamente.")
        return True
    else:
        messagebox.showerror("Error", "Código de verificación incorrecto.")
        return False

def login_user(email, password):
    if email in usuarios_registrados and usuarios_registrados[email]['password'] == password:
        messagebox.showinfo("Login", "Login exitoso.")
        return True
    else:
        messagebox.showerror("Error", "Credenciales incorrectas.")
        return False

# Interfaz gráfica con Tkinter

def mostrar_ventana_registro():
    ventana_registro = tk.Toplevel(root)
    ventana_registro.title("Registro")

    tk.Label(ventana_registro, text="Email").grid(row=0, column=0)
    tk.Label(ventana_registro, text="Nombre de usuario").grid(row=1, column=0)
    tk.Label(ventana_registro, text="Contraseña").grid(row=2, column=0)

    email_entry = tk.Entry(ventana_registro)
    username_entry = tk.Entry(ventana_registro)
    password_entry = tk.Entry(ventana_registro, show="*")

    email_entry.grid(row=0, column=1)
    username_entry.grid(row=1, column=1)
    password_entry.grid(row=2, column=1)

    def registrar():
        email = email_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        if register_user(email, username, password):
            ventana_registro.destroy()
            mostrar_ventana_verificacion(email)

    tk.Button(ventana_registro, text="Registrar", command=registrar).grid(row=3, columnspan=2)

def mostrar_ventana_verificacion(email):
    ventana_verificacion = tk.Toplevel(root)
    ventana_verificacion.title("Verificación")

    tk.Label(ventana_verificacion, text="Código de verificación").grid(row=0, column=0)

    codigo_entry = tk.Entry(ventana_verificacion)
    codigo_entry.grid(row=0, column=1)

    def verificar():
        codigo = codigo_entry.get()
        if verify_email(email, int(codigo)):
            ventana_verificacion.destroy()

    tk.Button(ventana_verificacion, text="Verificar", command=verificar).grid(row=1, columnspan=2)

def mostrar_ventana_login():
    ventana_login = tk.Toplevel(root)
    ventana_login.title("Login")

    tk.Label(ventana_login, text="Email").grid(row=0, column=0)
    tk.Label(ventana_login, text="Contraseña").grid(row=1, column=0)

    email_entry = tk.Entry(ventana_login)
    password_entry = tk.Entry(ventana_login, show="*")

    email_entry.grid(row=0, column=1)
    password_entry.grid(row=1, column=1)

    def iniciar_sesion():
        email = email_entry.get()
        password = password_entry.get()
        if login_user(email, password):
            ventana_login.destroy()

    tk.Button(ventana_login, text="Iniciar sesión", command=iniciar_sesion).grid(row=2, columnspan=2)

root = tk.Tk()
root.title("Sistema de Registro y Login")

tk.Button(root, text="Registrar", command=mostrar_ventana_registro).pack()
tk.Button(root, text="Iniciar sesión", command=mostrar_ventana_login).pack()

root.mainloop()

