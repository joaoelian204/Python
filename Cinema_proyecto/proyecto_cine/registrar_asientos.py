# registrar_asientos.py
import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
from colores import *
import login
from datetime import datetime
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from tempfile import NamedTemporaryFile
import pdfkit
import os
# Conectar a la base de datos de películas
conn_peliculas = sqlite3.connect('cartelera.db')
cursor_peliculas = conn_peliculas.cursor()

# Conectar a la base de datos de usuarios
conn_usuarios = sqlite3.connect('usuarios.db')
cursor_usuarios = conn_usuarios.cursor()

# Crear las tablas si no existen
cursor_peliculas.execute('''
CREATE TABLE IF NOT EXISTS peliculas (
    id INTEGER PRIMARY KEY,
    titulo TEXT,
    genero TEXT,
    duracion TEXT,
    imagen TEXT,
    sinopsis TEXT
)
''')

cursor_peliculas.execute('''
CREATE TABLE IF NOT EXISTS horarios (
    id INTEGER PRIMARY KEY,
    id_pelicula INTEGER,
    horario TEXT,
    sala TEXT,
    FOREIGN KEY (id_pelicula) REFERENCES peliculas (id)
)
''')

cursor_usuarios.execute('''
CREATE TABLE IF NOT EXISTS reservas (
    id INTEGER PRIMARY KEY,
    id_usuario INTEGER,
    id_pelicula INTEGER,
    hora TEXT,
    sala TEXT,
    asiento TEXT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios (id),
    FOREIGN KEY (id_pelicula) REFERENCES peliculas (id)
)
''')

# Variable global para almacenar los asientos seleccionados
asientos_seleccionados = {}

# Función para crear y mostrar el estado de los asientos
def crear_estado_asientos(frame):
    estado = {
        "simbolo": ("L", "O", "S"),
        "estados": ("Libre", "Ocupado", "Seleccionado"),
        "colores": (color_libre, color_ocupado, color_seleccionado)
    }
    for i in range(3):
        estado_frame = tk.Frame(frame, bg=color_fondo, bd=2, relief="groove")
        estado_frame.grid(row=i, column=0, pady=10, padx=10, sticky='ew')
        
        canvas_estado = tk.Canvas(estado_frame, width=20, height=20, bg=color_fondo, highlightthickness=0)
        canvas_estado.create_rectangle(2, 2, 18, 18, fill=estado['colores'][i])
        canvas_estado.pack(side=tk.LEFT, padx=5)
        
        tk.Label(estado_frame, text=f"{estado['simbolo'][i]}: {estado['estados'][i]}", bg=color_fondo, fg="black", font=fuente_estado_asiento).pack(side=tk.LEFT)

# Función para mostrar el registro de asientos
def mostrar_registro_asientos(cuerpo_principal, pelicula_id, hora, sala_index, usuario_id):
    # Limpiar el cuerpo_principal
    for widget in cuerpo_principal.winfo_children():
        widget.destroy()

    # Dividir el cuerpo principal en dos frames
    frame_izquierdo = tk.Frame(cuerpo_principal, bg="black")
    frame_izquierdo.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    frame_derecho = tk.Frame(cuerpo_principal, bg=color_fondo)
    frame_derecho.grid(row=0, column=1, sticky="nsew", padx=50, pady=20)

    cuerpo_principal.grid_columnconfigure(0, weight=3)
    cuerpo_principal.grid_columnconfigure(1, weight=1)
    cuerpo_principal.grid_rowconfigure(0, weight=1)

    # Obtener los asientos seleccionados para esta combinación de película, hora y sala
    key = (pelicula_id, hora, sala_index)

    if key not in asientos_seleccionados:
        asientos_seleccionados[key] = [[0]*11 for _ in range(11)]
    matriz_asientos = asientos_seleccionados[key]

    # Consultar las reservas existentes en la base de datos para marcarlas como ocupadas
    cursor_usuarios.execute('''
        SELECT asiento FROM reservas
        WHERE id_pelicula = ? AND hora = ? AND sala = ?
    ''', (pelicula_id, hora, sala_index))
    reservas_existentes = cursor_usuarios.fetchall()

    for reserva in reservas_existentes:
        asiento = reserva[0]
        fila = ord(asiento[0]) - ord('A')
        columna = int(asiento[1:]) - 1
        matriz_asientos[fila][columna] = 2

    img_libre = ImageTk.PhotoImage(Image.open("/home/joaoelian/Descargas/asientolibre.png").resize((60, 60)))
    img_ocupado = ImageTk.PhotoImage(Image.open("/home/joaoelian/Descargas/asientoocupado.png").resize((60, 60)))
    img_seleccionado = ImageTk.PhotoImage(Image.open("/home/joaoelian/Descargas/asientoseleccionado.png").resize((60, 60)))
    img_mejor_asiento = ImageTk.PhotoImage(Image.open("/home/joaoelian/Descargas/asientomejor.png").resize((60, 60)))
    
    def seleccionar_asiento(i, j):
        if 0 <= i < 11 and 0 <= j < 11:
            estado_actual = matriz_asientos[i][j]
            if estado_actual == 0:
                matriz_asientos[i][j] = 1
                botones_asientos[i][j].configure(image=img_seleccionado)
            elif estado_actual == 1:
                matriz_asientos[i][j] = 0
                botones_asientos[i][j].configure(image=img_libre)
            elif estado_actual == 2:
                messagebox.showerror("Error", "Este asiento ya está ocupado.")

    label_horarios = tk.Label(frame_izquierdo, text="Selecciona tus asientos", font=("Helvetica", 24, "bold"), fg=color_titulo, bg="black")
    label_horarios.pack(pady=(10, 20))

    frame_asientos = tk.Frame(frame_izquierdo, bg="black")
    frame_asientos.pack(expand=True)

    botones_asientos = []
    for i in range(11):
        fila_botones = []
        for j in range(11):
            boton = tk.Button(frame_asientos, image=img_libre, width=60, height=60, bd=2, relief="raised")
            boton.grid(row=i, column=j, padx=5, pady=5)
            boton.config(command=lambda i=i, j=j: seleccionar_asiento(i, j))
            if matriz_asientos[i][j] == 1:
                boton.config(image=img_seleccionado)
            elif matriz_asientos[i][j] == 2:
                boton.config(image=img_ocupado)
            fila_botones.append(boton)
        botones_asientos.append(fila_botones)

    def buscar_mejor_asiento():
        mejores_asientos = []
        for i in range(11):
            for j in range(11):
                if matriz_asientos[i][j] == 0:
                    mejores_asientos.append((i, j, abs(3 - i) + abs(3 - j)))
        mejores_asientos.sort(key=lambda x: x[2])
        for i in range(min(4, len(mejores_asientos))):
            fila, columna, _ = mejores_asientos[i]
            botones_asientos[fila][columna].configure(image=img_mejor_asiento)

    def confirmar_reservas():
        if usuario_id is None:
            messagebox.showerror("Error", "No se ha identificado el usuario.")
            return
        
        reservas = []
        asientos_confirmados = []
        for i in range(11):
            for j in range(11):
                if matriz_asientos[i][j] == 1:
                    matriz_asientos[i][j] = 2
                    botones_asientos[i][j].configure(image=img_ocupado)
                    fila = chr(i + ord('A'))
                    columna = j + 1
                    asiento = f"{fila}{columna}"
                    sala_numero = int(sala_index.replace('Sala ', ''))
                    reservas.append((usuario_id, pelicula_id, hora, f"Sala {sala_numero}", asiento))
                    asientos_confirmados.append(asiento)

        cursor_usuarios.executemany('INSERT INTO reservas (id_usuario, id_pelicula, hora, sala, asiento) VALUES (?, ?, ?, ?, ?)', reservas)
        conn_usuarios.commit()

        generar_ticket(usuario_id, pelicula_id, hora, f"Sala {sala_numero}", asientos_confirmados)
        messagebox.showinfo("Reservas Confirmadas", "¡Tus reservas han sido confirmadas!")
        
#================= Funciones de generación de ticket y envío de correo =================================================================

    def generar_ticket(usuario_id, pelicula_id, hora, sala, asientos):
        usuario_nombre = obtener_nombre_usuario(usuario_id)
        fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pelicula_nombre = obtener_nombre_pelicula(pelicula_id)
    
        ticket_texto = (
            f"CINEMA MANTA\n"
            f"------------------------\n"
            f"Usuario: {usuario_nombre}\n"
            f"Película: {pelicula_nombre}\n"
            f"Hora: {hora}\n"
            f"Sala: {sala}\n"
            f"Asientos: {', '.join(asientos)}\n"
            f"Fecha y Hora: {fecha_hora_actual}\n"
            f"------------------------\n"
            f"¡Disfruta la película!\n"
                )
    
        ticket_display.delete(1.0, tk.END)
        ticket_display.insert(tk.END, ticket_texto)

        guardar_ticket(usuario_nombre, {
            "usuario": usuario_nombre,
            "pelicula": pelicula_nombre,
            "hora": hora,
            "sala": sala,
            "asientos": asientos,
            "fecha_hora": fecha_hora_actual
            })

        generar_pdf_ticket(usuario_nombre, pelicula_nombre, hora, sala, asientos, fecha_hora_actual)
        enviar_correo(usuario_id, "ticket.pdf")


    def obtener_nombre_usuario(usuario_id):
        cursor_usuarios.execute('SELECT nombre FROM usuarios WHERE id = ?', (usuario_id,))
        resultado = cursor_usuarios.fetchone()
        return resultado[0] if resultado else "Desconocido"
    
    def obtener_nombre_pelicula(pelicula_id):
        cursor_peliculas.execute('SELECT titulo FROM peliculas WHERE id = ?', (pelicula_id,))
        resultado = cursor_peliculas.fetchone()
        return resultado[0] if resultado else "Desconocido"

    def guardar_ticket(usuario_nombre, ticket_info):
        try:
            with open('tickets.json', 'r') as file:
                tickets = json.load(file)
        except FileNotFoundError:
            tickets = {}
        
        if usuario_nombre not in tickets:
            tickets[usuario_nombre] = []

        tickets[usuario_nombre].append(ticket_info)

        with open('tickets.json', 'w') as file:
            json.dump(tickets, file, indent=4)


    def generar_pdf_ticket(usuario_nombre, pelicula_nombre, hora, sala, asientos, fecha_hora):
        # Ruta de la imagen del logo
        logo_path = "https://img.freepik.com/vector-premium/plantilla-diseno-logotipo-pelicula-rollo-camara-cine_527727-210.jpg"
        
        html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
                text-align: center;
            }}
            .ticket {{
                width: 80%;
                margin: 50px auto;
                padding: 20px;
                background-color: #fff;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                margin-bottom: 20px;
            }}
            .logo {{
                width: 250px;
                margin-bottom: 200px;
            }}
            .details {{
                text-align: left;
                margin: 20px 0;
            }}
            .details p {{
                margin: 5px 0;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 14px;
                color: #888;
            }}
        </style>
    </head>
    <body>
        <div class="ticket">
            <img src="{logo_path}" alt="Logo" class="logo">
            <h1>CINEMA MANTA</h1>
            <hr>
            <div class="details">
                <p><strong>Usuario:</strong> {usuario_nombre}</p>
                <p><strong>Película:</strong> {pelicula_nombre}</p>
                <p><strong>Hora:</strong> {hora}</p>
                <p><strong>Sala:</strong> {sala}</p>
                <p><strong>Asientos:</strong> {', '.join(asientos)}</p>
                <p><strong>Fecha y Hora:</strong> {fecha_hora}</p>
            </div>
            <hr>
            <div class="footer">
                <p>¡Disfruta la película!</p>
            </div>
        </div>
    </body>
    </html>
    """
    
        with NamedTemporaryFile(delete=False, suffix='.html') as temp_html:
            temp_html.write(html_content.encode('utf-8'))
            temp_html_path = temp_html.name
    
        pdf_output_path = os.path.join(os.getcwd(), "ticket.pdf")
        pdfkit.from_file(temp_html_path, pdf_output_path)
    
        os.remove(temp_html_path)  # Eliminar el archivo HTML temporal


    def enviar_correo(usuario_id, archivo_pdf):
        cursor_usuarios.execute('SELECT correo FROM usuarios WHERE id = ?', (usuario_id,))
        resultado = cursor_usuarios.fetchone()
        if resultado:
            correo_usuario = resultado[0]
        else:
            messagebox.showerror("Error", "No se pudo encontrar el correo del usuario.")
            return

        remitente = "cineprueba34@gmail.com"
        admin = "Administrador de Cinema Manta"
        password = "uboy coxy skrv ibsa"
        destinatario = correo_usuario
        asunto = "Tu Ticket de Cine"
        ruta_imagen = 'https://i.ibb.co/GMs89QG/CIIIIIIIIIneeee.png'
        
        cuerpo = f"""\
                <html>
                    <body>
                        <p>Hola otra vez 😊.</p>
                        <p>Te adjunto aquí tu ticket para la función 🎟️. ¡Que disfrutes de la película..!🍿</p>
                        <p>Saludos,<br>
                        Administrador de Cinema Manta</p>
                        <p><b>Mensaje generado automáticamente. Por favor no responder a este correo.</b></p>
                        <img src="{ruta_imagen}" alt="Imagen de presentación">
                    </body>
                </html>
                """


        mensaje = MIMEMultipart()
        mensaje['From'] = admin
        mensaje['To'] = destinatario
        mensaje['Subject'] = asunto

        mensaje.attach(MIMEText(cuerpo, 'html'))

        adjunto = MIMEBase('application', 'octet-stream')
        adjunto.set_payload(open(archivo_pdf, "rb").read())
        encoders.encode_base64(adjunto)
        adjunto.add_header('Content-Disposition', f'attachment; filename={archivo_pdf}')
        mensaje.attach(adjunto)

        try:
            servidor = smtplib.SMTP('smtp.gmail.com', 587)
            servidor.starttls()
            servidor.login(remitente, password)
            texto = mensaje.as_string()
            servidor.sendmail(remitente, destinatario, texto)
            servidor.quit()
            messagebox.showinfo("Correo Enviado", f"Su ticket ha sido guardado y enviado a su correo electronico automaticamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el correo: {str(e)}")

    crear_estado_asientos(frame_derecho)
    
    boton_confirmar = tk.Button(frame_derecho, text="Guardar Selección", fg=COLOR_TEXTO_NORMAL, bg=COLOR_BOTON_NORMAL, font=("Helvetica", 16), bd=2, relief="raised", command=confirmar_reservas)
    boton_confirmar.grid(row=3, column=0, pady=10, sticky='ew')

    boton_buscar_mejor = tk.Button(frame_derecho, text="Buscar Mejor Asiento", fg=COLOR_TEXTO_NORMAL, bg=COLOR_BOTON_NORMAL, font=("Helvetica", 16), bd=2, relief="raised", command=buscar_mejor_asiento)
    boton_buscar_mejor.grid(row=4, column=0, pady=10, sticky='ew')

    ticket_display = tk.Text(frame_derecho, height=10, width=50, bg="white", fg="black", font=("Helvetica", 12), bd=2, relief="sunken")
    ticket_display.grid(row=5, column=0, pady=10, sticky='ew')
















