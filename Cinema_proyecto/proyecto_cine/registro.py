import tkinter as tk
import sqlite3
from tkinter import messagebox
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randint

# Configuración del servidor SMTP
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL = 'cineprueba34@gmail.com'
PASSWORD = 'uboy coxy skrv ibsa'

# Base de datos temporal de usuarios
usuarios_temporales = {}
usuarios_registrados = {}
#funcion para obtener el nombre de usuario
def obtener_nombre_usuario(email):
    """
    Obtiene el nombre de usuario basado en el email.
    Primero verifica en usuarios registrados, luego en usuarios temporales.
    """
    if email in usuarios_registrados:
        return usuarios_registrados[email]['username']
    elif email in usuarios_temporales:
        return usuarios_temporales[email]['username']
    else:
        return "Usuario"
#funcion para enviar correo de verificacion
def enviar_correo_verificacion(destinatario, codigo_verificacion):
    """
    Envía un correo de verificación al destinatario con un código de verificación.
    """
    # Configuración del correo
    admin = 'Administrador de Cinema Manta'
    asunto = 'Verificación de correo'
    nombre_destinatario = obtener_nombre_usuario(destinatario[0])
    ruta_imagen_local = 'https://i.ibb.co/jTx9g25/cinema.png'
    # Mensaje del correo
    mensaje = f'''<html>
                    <head></head>
                    <body>
                        <p>Hola {nombre_destinatario},</p>
                        <p>¡Gracias por registrarte en nuestro cine! Para completar el proceso de 
                        verificación de tu cuenta, por favor utiliza el siguiente código de verificación:</p>
                        <p><b>{codigo_verificacion}</b></p>
                        <p>Este código es válido por los próximos 30 minutos. Si no solicitaste este código,
                        por favor ignora este correo.</p>
                        <p>Si tienes alguna pregunta o necesitas asistencia adicional, no dudes en contactarnos.
                        ¡Esperamos verte pronto en nuestras salas de cine disfrutando de las mejores películas!</p>
                        <p>Saludos cordiales,<br>
                        Administrador de Cinema Manta</p>
                        <p><b> Mensaje generado automáticamente. Por favor no responder a este correo.</b></p>
                        <img src="{ruta_imagen_local}" alt="Imagen de presentación">
                    </body>
                </html>'''
#crea la instancia del mensaje
    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = admin
    msg['To'] = ', '.join(destinatario)
    msg['Subject'] = asunto
    msg.attach(MIMEText(mensaje, 'html'))
    # Enviar el mensaje
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, destinatario, msg.as_string())
            print('Correo enviado exitosamente')
    except smtplib.SMTPAuthenticationError as e:
        print(f'Error de autenticación: {e}')
        messagebox.showerror("Error de Autenticación", "No se pudo autenticar con el servidor SMTP. Verifica tus credenciales.")
    except Exception as e:
        print(f'Error al enviar correo: {e}')
        messagebox.showerror("Error", f"No se pudo enviar el correo: {e}")
#funcion para registrar usuario
def registrar_usuario(email, username, password, genero):
    """
    Registra un usuario temporalmente y envía un correo de verificación.
    """
    if email in usuarios_registrados:
        messagebox.showerror("Error", "El correo ya está registrado.")
        return False
    # Generar un código de verificación aleatorio
    # y almacenar los datos del usuario temporalmente
    # randint() genera un número aleatorio entre 100000 y 999999
    codigo_verificacion = randint(100000, 999999)
    usuarios_temporales[email] = {
        'username': username,
        'password': password,
        'genero': genero,
        'codigo_verificacion': codigo_verificacion
    }
    # Enviar correo de verificación
    enviar_correo_verificacion([email], codigo_verificacion)
    messagebox.showinfo("Registro", "Usuario registrado temporalmente. Verifica tu correo.")
    return True
#funcion para verificar correo
def verificar_correo(email, codigo_verificacion):
    """
    Verifica el correo del usuario con el código de verificación proporcionado.
    """
    # Verificar si el email y el código de verificación coinciden
    if email in usuarios_temporales and usuarios_temporales[email]['codigo_verificacion'] == codigo_verificacion:
        usuario = usuarios_temporales[email]
        guardar_datos(usuario['username'], email, usuario['password'], usuario['genero'])
        usuarios_registrados[email] = usuario
        del usuarios_temporales[email]
        messagebox.showinfo("Verificación", "Correo verificado y usuario registrado exitosamente.")
        return True
    else:
        messagebox.showerror("Error", "Código de verificación incorrecto.")
        return False
#funcion para iniciar sesion de usuario
def iniciar_sesion_usuario(email, password):
    """
    Inicia sesión del usuario verificando sus credenciales.
    """
    # Verificar las credenciales del usuario
    usuario_registrado = verificar_credenciales(email, password)
    if usuario_registrado:
        messagebox.showinfo("Login", "Login exitoso.")
        return True
    else:
        messagebox.showerror("Error", "Credenciales incorrectas.")
        return False
#funcion para guardar datos
def guardar_datos(nombre, correo, contraseña, genero):
    """
    Guarda los datos del usuario en la base de datos SQLite.
    """
    # Conectar a la base de datos
    conexion = sqlite3.connect('usuarios.db')
    cursor = conexion.cursor()
    # Crear la tabla si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, correo TEXT, contraseña TEXT, genero TEXT)''')
    # Insertar los datos del usuario
    cursor.execute("INSERT INTO usuarios (nombre, correo, contraseña, genero) VALUES (?, ?, ?, ?)",
                (nombre, correo, contraseña, genero))
    conexion.commit()
    # Obtener el ID del usuario recién insertado
    user_id = cursor.lastrowid
    # Cerrar la conexión y mostrar un mensaje de éxito
    messagebox.showinfo("Registro exitoso", "Registro guardado correctamente")
    # Cerrar la conexión
    cursor.close()
    conexion.close()
    # Retornar el ID del usuario
    return user_id
#funcion para verificar credenciales
def verificar_credenciales(usuario, contraseña):
    """
    Verifica las credenciales del usuario en la base de datos SQLite.
    """
    # Conectar a la base de datos
    conexion = sqlite3.connect('usuarios.db')
    cursor = conexion.cursor()
# Consultar la base de datos para verificar las credenciales
    cursor.execute("SELECT * FROM usuarios WHERE correo=? AND contraseña=?", (usuario, contraseña))
    usuario_registrado = cursor.fetchone()

    cursor.close()
    conexion.close()

    return usuario_registrado
#funcion para abrir ventana de registro
def abrir_ventana_registro():
    """
    Abre la ventana de registro de usuario.
    """
    # Crear la ventana de registro
    ventana_registro = tk.Toplevel()
    ventana_registro.title("Formulario de Registro")
    ventana_registro.geometry("450x300")
    ventana_registro.configure(bg="#2c3e50")
    ventana_registro.resizable(False, False)
# Crear los campos del formulario
    # Nombre de usuario
    label_nombre = tk.Label(ventana_registro, text="Nombre de usuario:", bg="#2c3e50", fg="#ecf0f1")
    label_nombre.grid(row=0, column=0, padx=10, pady=5)
    entry_nombre = tk.Entry(ventana_registro, width=30)
    entry_nombre.grid(row=0, column=1, padx=10, pady=5)
    # Correo electrónico
    label_correo = tk.Label(ventana_registro, text="Correo electrónico:", bg="#2c3e50", fg="#ecf0f1")
    label_correo.grid(row=1, column=0, padx=10, pady=5)
    entry_correo = tk.Entry(ventana_registro, width=30)
    entry_correo.grid(row=1, column=1, padx=10, pady=5)
    # Contraseña
    label_contraseña = tk.Label(ventana_registro, text="Contraseña:", bg="#2c3e50", fg="#ecf0f1")
    label_contraseña.grid(row=2, column=0, padx=10, pady=5)
    entry_contraseña = tk.Entry(ventana_registro, show="*", width=30)
    entry_contraseña.grid(row=2, column=1, padx=10, pady=5)
    # Género
    label_genero = tk.Label(ventana_registro, text="Género:", bg="#2c3e50", fg="#ecf0f1")
    label_genero.grid(row=3, column=0, padx=10, pady=5)
    genero_var = tk.StringVar(value="No especificado")
    opciones_genero = ["Hombre", "Mujer", "Otros", "No especificado"]
    entry_genero = tk.OptionMenu(ventana_registro, genero_var, *opciones_genero)
    entry_genero.grid(row=3, column=1, padx=10, pady=5)
    # Función para guardar el registro del usuario
    def guardar_registro():
        """
        Guarda el registro del usuario después de validar los campos del formulario.
        """
        # Obtener los valores de los campos del formulario
        nombre = entry_nombre.get().strip()
        correo = entry_correo.get().strip()
        contraseña = entry_contraseña.get().strip()
        genero = genero_var.get()
        # Validar los campos del formulario
        if nombre == "" or contraseña == "" or correo == "":
            messagebox.showerror("Error", "Por favor, complete todos los campos del formulario.")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            messagebox.showerror("Error", "Ingrese un correo electrónico válido.")
        else:
            if registrar_usuario(correo, nombre, contraseña, genero):
                ventana_registro.destroy()
                mostrar_ventana_verificacion(correo)
    # Botón para guardar el registro
    boton_guardar = tk.Button(ventana_registro, text="Registrar", command=guardar_registro, width=30, bg="blue", fg="white")
    boton_guardar.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="WE")
#funcion para mostrar ventana de verificacion
def mostrar_ventana_verificacion(email):
    """
    Muestra la ventana para que el usuario ingrese el código de verificación enviado por correo.
    """
    # Crear la ventana de verificación
    ventana_verificacion = tk.Toplevel()
    ventana_verificacion.title("Verificación de Correo")
    ventana_verificacion.geometry("370x100")
    ventana_verificacion.configure(bg="#2c3e50")
    ventana_verificacion.resizable(False, False)
    # Etiqueta y campo de entrada para el código de verificación
    tk.Label(ventana_verificacion, text="Código de verificación:", bg="#2c3e50", fg="#ecf0f1").grid(row=0, column=0, padx=10, pady=5)
    codigo_entry = tk.Entry(ventana_verificacion)
    codigo_entry.grid(row=0, column=1, padx=10, pady=5)
    # Función para verificar el código de verificación
    def verificar():
        """
        Verifica el código de verificación ingresado por el usuario.
        """
        # Obtener el código de verificación ingresado por el usuario
        codigo = codigo_entry.get().strip()
        if codigo == "":
            messagebox.showerror("Error", "Por favor, ingrese el código de verificación.")
        else:
            try:
                if verificar_correo(email, int(codigo)):
                    ventana_verificacion.destroy()
            except ValueError:
                messagebox.showerror("Error", "El código de verificación debe ser un número.")
    # Botón para verificar el código de verificación
    tk.Button(ventana_verificacion, text="Verificar", command=verificar, width=20, bg="green", fg="white").grid(row=1, columnspan=2, padx=10, pady=10)





